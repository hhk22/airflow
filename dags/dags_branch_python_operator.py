import pendulum
import random

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator

with DAG(
    dag_id="dags_branch_python_operator",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    def select_random():
        import random

        item_lst = ["A", "B", "C"]
        selected_item = random.choice(item_lst)
        if selected_item == "A":
            return "task_a"
        else:
            return ["task_b", "task_c"]

    python_branch_task = BranchPythonOperator(
        task_id="python_branch_task",
        python_callable=select_random
    )

    def common_func(**kwargs):
        print(kwargs['selected'])
    
    task_a = PythonOperator(
        task_id="task_aa",
        python_callable=common_func,
        op_kwargs={"selected":"A"}
    )

    task_b = PythonOperator(
        task_id="task_bb",
        python_callable=common_func,
        op_kwargs={"selected":"B"}
    )
    task_c = PythonOperator(
        task_id="task_cc",
        python_callable=common_func,
        op_kwargs={"selected":"C"}
    )

    python_branch_task >> [task_a, task_b, task_c]