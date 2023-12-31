import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task

with DAG(
    dag_id="dags_branch_python_decorator",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    @task.branch(task_id="python_branch_task")
    def select_random():
        import random

        item_lst = ["A", "B", "C"]
        selected_item = random.choice(item_lst)
        if selected_item == "A":
            return "task_a"
        else:
            return ["task_b", "task_c"]


    def common_func(**kwargs):
        print(kwargs['selected'])
    
    task_a1 = PythonOperator(
        task_id="task_a",
        python_callable=common_func,
        op_kwargs={"selected":"A"}
    )

    task_b1 = PythonOperator(
        task_id="task_b",
        python_callable=common_func,
        op_kwargs={"selected":"B"}
    )
    task_c1 = PythonOperator(
        task_id="task_c",
        python_callable=common_func,
        op_kwargs={"selected":"C"}
    )

    select_random() >> [task_a1, task_b1, task_c1]