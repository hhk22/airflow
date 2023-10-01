import datetime
import random
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from common.common_func import get_sftp

with DAG(
    dag_id="dags_sftp_operator",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    py_t1 = PythonOperator(
        task_id="py_t1",
        python_callable=get_sftp
    )

    py_t1