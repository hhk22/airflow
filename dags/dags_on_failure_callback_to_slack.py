from airflow import Dataset
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
from common.on_failure_callback_to_slack import on_failure_callback_to_slack
import pendulum

dataset_dags_dataset_producer_1 = Dataset("dags_dataset_producer_1")

with DAG(
        dag_id='dags_on_failure_callback_to_slack',
        schedule=[dataset_dags_dataset_producer_1],
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        default_args={
            "on_failure_callback": on_failure_callback_to_slack,
            "execution_timeout": timedelta(seconds=60)
        },
        catchup=False
) as dag:

    task_slp_90 = BashOperator(
        task_id="sleep_90",
        bash_command="sleep 90"
    )

    task_ext_1 = BashOperator(
        trigger_rule="all_done"
        task_id="task_exit_1",
        bash_command="exit 1"
    )

    task_slp_90 >> task_ext_1