import datetime
import pendulum

from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="dags_with_xcom_eg2",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task(task_id="python_xcom_push_task1")
    def xcom_push1(**kwargs):
        return 'Success'
    
    @task(task_id="python_xcom_push_task2")
    def xcom_pull_1(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(task_ids="python_xcom_push_task1")
    
    @task(task_id="python_xcom_pull_task")
    def xcom_pull_2(status, **kwargs):
        print('status >> ', status)
    
    xcom_push_return = xcom_push1()
    xcom_pull_2(xcom_push_return)
    xcom_push_return >> xcom_pull_1()
    

    