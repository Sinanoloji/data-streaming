from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from producer import produce_to_kafka

start_date = datetime(2024,10,8)

default_args = {
    "owner": "airflow",
    "start_date": start_date,
    "retries": 1,
    "retry_delay": timedelta(seconds=5)
}


with DAG("my_people",default_args=default_args,schedule='0 1 * * *', catchup=False) as dag:
    data_stream_task = PythonOperator(
        task_id="kafka_data_stream",
        python_callable=produce_to_kafka,
        dag=dag
    )

    data_stream_task