import datetime
import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_bash_python_with_xcom",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:

    bash_push = BashOperator(
        task_id = "bash_push",
        bash_command="echo START &&"
                     "echo {{ ti.xcom_push(key='bash_pushed', value=200) }} &&"
                     "echo FINISHED"
    )

    @task(task_id="python_pull")
    def python_pull(**kwargs):
        ti = kwargs['ti']
        start_value = ti.xcom_pull(key='bash_pushed')
        finish_value = ti.xcom_pull(task_ids='bash_push')
        print(start_value)
        print(finish_value)
    
    bash_push >> python_pull()

