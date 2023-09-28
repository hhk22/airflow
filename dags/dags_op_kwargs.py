import datetime
import random
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from common.common_func import regist2

with DAG(
    dag_id="dags_python_with_kwargs",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    
    regist_t1 = PythonOperator(
        task_id="regist_t1",
        python_callable=regist2,
        op_args=["hjkim", "man", "kr", "seoul"],
        op_kwargs={"email": 'khhh9401@gmail.com', "phone": "010"}
    )

    regist_t1
