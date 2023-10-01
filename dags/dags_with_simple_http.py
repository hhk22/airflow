# apikey_openapi_seoul

import datetime

import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

with DAG(
    dag_id="dags_with_simple_http",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    

    simple_http_task = SimpleHttpOperator(
        task_id="simple_http_task",
        http_conn_id="openapi.seoul.go.kr",
        endpoint="{{var.value.apikey_openapi_seoul}}/json/TbParkingInfoView/1/10/",
        method="GET",
        headers={
            'Content-Type': 'application/json',
            'charset': 'utf-8',
            'Accept': '*/*'
        }
    )

    @task(task_id="python_task")
    def python_task(**kwargs):
        ti = kwargs['ti']
        result = ti.xcom_pull(task_ids="simple_http_task")
        import json
        from pprint import pprint

        pprint(json.loads(result))
    
    simple_http_task >> python_task()