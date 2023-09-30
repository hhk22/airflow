import datetime
import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_python_bash_with_xcom",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    

    @task(task_id="python_bash")
    def python_push_xcom():
        return {
            "status": "Good",
            "data": [1, 2, 3],
            "options_cnt": 100
        }

    bash_pull = BashOperator(
        task_id="bash_pull",
        env= {
            "STATUS": "{{ti.xcom_pull(task_ids='python_bash')['status']}}",
            "DATA": "{{ti.xcom_pull(task_ids='python_bash')['data']}}",
            "OPTIONS_CNT": "{{ti.xcom_pull(task_ids='python_bash')['options_cnt']}}"
        },
        bash_command="echo $STATUS && echo $DATA && echo $OPTIONS_CNT"
    )

    python_push_xcom() >> bash_pull