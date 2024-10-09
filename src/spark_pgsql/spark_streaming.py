from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType,StructField,StringType, IntegerType, FloatType
from pyspark.sql.functions import from_json,col
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")

def create_spark_session() -> SparkSession:
    spark = SparkSession\
            .builder\
            .appName("PostgreSQL Connection with PySark")\
            .config("spark.jars.packages",
            "org.postgresql:postgresql:42.5.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",)\
            .config("spark.sql.adaptive.enabled", "false")\
            .getOrCreate()
    
    logging.info("Spark session created successfully")
    return spark

def create_initial_dataframe(spark_session: SparkSession) -> DataFrame:

    try:
        
        df = spark_session.readStream.format("kafka")\
            .option("kafka.bootstrap.servers","localhost:9094")\
            .option("subscribe","mytopic")\
            .option("startingOffsets", "earliest")\
            .option("kafka.sasl.mechanism", "SCRAM-SHA-256")\
            .load()
        logging.info("Initial dataframe crated successfully")
    except Exception as e:
        logging.warning(f"Initial dataframe couldn't : {e}")
        raise

    return df

def create_final_dataframe(df: DataFrame):

    schema = StructType([
                StructField("full_name",StringType(),False),
                StructField("gender",StringType(),False),
                StructField("location",StringType(),False),
                StructField("city",StringType(),False),
                StructField("country",StringType(),False),
                StructField("postcode",IntegerType(),False),
                StructField("latitude",FloatType(),False),
                StructField("longitude",FloatType(),False),
                StructField("email",StringType(),False)
            ])
    df_out = (
        df.selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"),schema).alias("data"))
        .select("data.*")
        
    )
    
    query = df_out.writeStream.foreachBatch(postgress_function).start()
    return query


def postgress_function(df:DataFrame,epoch):
    df.write.format("jdbc")\
        .option("url","jdbc:postgresql://localhost:5432/stream")\
        .option("driver","org.postgresql.Driver").option("dbtable","my_people")\
        .option("user","postgres").option("password","root").save()


if __name__ == "__main__":
    spark = create_spark_session()
    df = create_initial_dataframe(spark)
    query = create_final_dataframe(df)
    query.awaitTermination()
