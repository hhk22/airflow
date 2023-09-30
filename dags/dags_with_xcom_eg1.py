import datetime
import pendulum

from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="dags_with_xcom_eg1",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task(task_id="python_xcom_push_task1")
    def xcom_push1(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(key="result1", value="value_1")
        ti.xcom_push(key="result2", value=[1,2,3])
    
    @task(task_id="python_xcom_push_task2")
    def xcom_push2(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(key="result1", value="value_2")
        ti.xcom_push(key="result2", value=[1,2,3,4])
    
    @task(task_id="python_xcom_pull_task")
    def xcom_pull(**kwargs):
        ti = kwargs['ti']
        result1 = ti.xcom_pull(key="result1", task_ids='python_xcom_push_task1')
        result2 = ti.xcom_pull(key="result2", task_ids='python_xcom_push_task1')
        print(result1, result2)
    

    xcom_push1() >> xcom_push2() >> xcom_pull()