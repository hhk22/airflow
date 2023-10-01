import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_shell_test",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    
    t1_orange = BashOperator(
        task_id="t1_orange",
           bash_command="/opt/airflow/plugins/shell/select_fruit.sh ORANGE"
    )

    t2_avocado = BashOperator(
        task_id="t2_avocado",
           bash_command="/opt/airflow/plugins/shell/select_fruit.sh AVOCADO"
    )

    t1_orange >> t2_avocado