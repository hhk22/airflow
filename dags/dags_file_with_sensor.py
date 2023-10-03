# conn_id: conn_file_sensor

from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_file_with_sensor',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule='0 6 * * *',
    catchup=False
) as dag:
    
    task_sensor = FileSensor(
        task_id="file_sensor",
        fs_conn_id="conn_file_sensor",
        filepath='tvCorona19VaccinestatNew/20231001/tvCorona19VaccinestatNew.csv',
        recursive=False,
        poke_interval=60,
        timeout=60*60*24, # 1일
        mode='reschedule'
    )

    task_sensor