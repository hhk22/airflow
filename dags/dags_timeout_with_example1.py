from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum
from airflow.models import Variable


with DAG(
    dag_id='dags_timeout_with_example1',
    start_date=pendulum.datetime(2023, 5, 1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False,
    default_args={
        'email': "khhh9401@gmail.com",
        "email_on_failure": True,
        "execution_timeout": timedelta(seconds=20)
    }
) as dag:
    
    bash_sleep_30 = BashOperator(
        task_id="bash_sleep_30",
        bash_command="sleep 30"
    )

    bash_sleep_10 = BashOperator(
        task_id="bash_sleep_10",
        trigger_rule="all_done",
        bash_command="sleep 10"
    )

    bash_sleep_30 >> bash_sleep_10