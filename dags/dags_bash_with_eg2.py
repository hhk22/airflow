import datetime
import random
import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from dateutil import relativedelta

with DAG(
    dag_id="dags_bash_with_eg1",
    schedule="* * * * 6#2",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:

    bash_task_t1 = BashOperator(
        task_id = "bash_task_2",
        env= {
            "START_DATE": "{{data_interval_start.in_timezone('Asia/Seoul') - macros.dateutil.relativedelta.relativedelta(days=19)|ds}}",
            "END_DATE": "{{data_interval_end.in_timezone('Asia/Seoul') - macros.dateutil.relativedelta.relativedelta(days=14)|ds}}"
        },
        bash_command="echo $START_DATE && echo $END_DATE"
    )

    bash_task_t1