import pendulum
import random

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator

with DAG(
    dag_id="dags_with_trigger",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task.branch(task_id="branching")
    def select_random():
        import random

        item_lst = ["A", "B", "C"]
        selected_item = random.choice(item_lst)
        if selected_item == "A":
            return "task_a"
        elif selected_item == "B":
            return "task_b"
        else:
            return "task_c"
    
    @task(task_id="task_a")
    def task_a():
        print('success')

    @task(task_id="task_b")
    def task_b():
        print('success')

    @task(task_id="task_c")
    def task_c():
        print('success')

    @task(task_id="task_d", trigger_rule="none_skipped")
    def task_d():
        print('success')
    
    select_random() >> [task_a(), task_b(), task_c()] >> task_d()

    