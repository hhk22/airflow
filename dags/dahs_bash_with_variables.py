import datetime
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable

with DAG(
    dag_id="dags_bash_with_variables",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    var_value = Variable.get('sample_key')
    bash_task1 = BashOperator(
        task_id = "bash_task1",
        bash_command = f"echo variable:{var_value}"
    )

    bash_task2 = BashOperator(
        task_id = "bash_task2",
        bash_command="echo variable: {{var.value.sample_key }}"
    )

    bash_task1 >> bash_task2

