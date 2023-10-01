import datetime
import random
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="dags_python_operator_with_template",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    def python_function(start_date, end_date, **kwargs):
        print(start_date, end_date)
    
    python_t1 = PythonOperator(
        task_id="python_t1",
        python_callable=python_function,
        op_kwargs={'start_date': '{{data_interval_start|ds}}', 'end_date': '{{data_interval_end|ds}}'}
    )
