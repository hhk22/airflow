import datetime
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_bash_with_xcom",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    task_push = BashOperator(
        task_id="dags_bash_with_xcom_push",
        bash_command="echo START &&"
                     "echo {{ ti.xcom_push(key='bash_pushed', value='test') }} &&"
                     "echo COMPLETE"
    )

    task_pull = BashOperator(
        task_id="dags_bash_with_pull",
        env={
                "PUSHED": "{{ti.xcom_pull(key='bash_pushed')}}",
                "RETURNED": "{{ti.xcom_pull(task_ids=dags_bash_with_xcom_push)}}"
            },
        bash_command="echo $PUSHED && $RETURNED",
        do_xcom_push=False
    )

    task_push >> task_pull