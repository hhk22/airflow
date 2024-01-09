import datetime
import random
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from plugins.operators.stock_report_crawler import FinanceReportOperator

with DAG(
    dag_id="dags_stock_reporter",
    schedule="0 9 * * *",
    start_date=pendulum.datetime(2024, 1, 8, tz="Asia/Seoul"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    
    report_task = FinanceReportOperator(
        task_id="finance_stock_task"
    )
    
    report_task()