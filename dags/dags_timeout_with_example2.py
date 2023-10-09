from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum
from airflow.models import Variable


with DAG(
    dag_id='dags_sla_email_example',
    start_date=pendulum.datetime(2023, 5, 1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(minutes=1),
    default_args={
        'email': "khhh9401@gmail.com",
        "email_on_failure": True,
        "execution_timeout": timedelta(seconds=40)
    }
) as dag:
    
    bash_sleep_35 = BashOperator(
        task_id="bash_sleep_35",
        bash_command="sleep 35"
    )

    bash_sleep_36 = BashOperator(
        task_id="bash_sleep_36",
        trigger_rule="all_done",
        bash_command="sleep 36"
    )

    bash_go = BashOperator(
        task_id="bash_go",
        bash_command="exit 0"
    )

    bash_sleep_35 >> bash_sleep_36 >> bash_go