import datetime
import random
import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from common.common_func import get_sftp

with DAG(
    dag_id="dags_task_decorator",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task(task_id="python_task_1")
    def print_context(some_input):
        print(some_input)
    
    python_task_1 = print_context("task decorator execute")
