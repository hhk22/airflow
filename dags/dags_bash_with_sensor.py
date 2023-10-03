from airflow.sensors.bash import BashSensor
from airflow.operators.bash import BashOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_bash_sensor',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule='0 6 * * *',
    catchup=False
) as dag:

    sensor_task_by_poke = BashSensor(
        task_id="sensor_task_by_poke",
        bash_command="echo task1 && exit 0",
        poke_interval=10,
        timeout=10,
        mode="poke",
        soft_fail=False
    )

    sensor_task_by_reschedule = BashSensor(
        task_id="sensor_task_by_reschedule",
        bash_command="echo task1 && exit 0",
        poke_interval=10,
        timeout=10,
        mode="reschedule",
        soft_fail=False
    )

    bash_task = BashOperator(
        task_id="bash_operator",
        bash_command="echo bash task done"
    )

    [sensor_task_by_poke, sensor_task_by_reschedule] >> bash_task

