from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os


sys.path.append(os.path.join(os.getcwd(), 'src'))
from kafka_client.producer import produce_to_kafka
from spark_pgsql.spark_streaming import start_streaming

start_date = datetime(2024,10,8)


default_args = {
    "owner": "airflow",
    "start_date": start_date,
    "retries": 1,
    "retry_delay": timedelta(seconds=5)
}


with DAG("random_people_names",default_args=default_args,schedule='0 1 * * *', catchup=False) as dag:

    data_streaming = PythonOperator(
        task_id="produce_to_topic",
        python_callable=produce_to_kafka,
        dag=dag,
    )

    spark_streaming = PythonOperator(
        task_id="start_streaming",
        python_callable=start_streaming,
        dag=dag,
    )

    data_streaming >> spark_streaming
