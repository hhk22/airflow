import datetime

import pendulum

from airflow import DAG
from airflow.operators.email import EmailOperator

with DAG(
    dags_id="dags_email_operator",
    schedule="0 8 1 * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    send_email_task = EmailOperator(
        task_id="send_email_task",
        to="khhh1499@gmail.com",
        subject="Airflow authroization",
        html_content="Airflow authroization done successfully"
    )