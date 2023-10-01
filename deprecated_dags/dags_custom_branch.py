from typing import Iterable
from airflow.utils.context import Context
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.branch import BaseBranchOperator
from airflow.decorators import task

with DAG(
    dag_id="dags_custom_branch",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 9, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    class CustomBranchOperator(BaseBranchOperator):
        def choose_branch(self, context: Context):
            import random

            item_lst = ["A", "B", "C"]
            selected_item = random.choice(item_lst)
            if selected_item == "A":
                return "task_a"
            else:
                return ["task_b", "task_c"]
        
    def common_func(**kwargs):
        print(kwargs['selected'])
    
    task_a = PythonOperator(
        task_id="task_a",
        python_callable=common_func,
        op_kwargs={"selected":"A"}
    )

    task_b = PythonOperator(
        task_id="task_b",
        python_callable=common_func,
        op_kwargs={"selected":"B"}
    )
    task_c = PythonOperator(
        task_id="task_c",
        python_callable=common_func,
        op_kwargs={"selected":"C"}
    )
        
    custom_branch_operator = CustomBranchOperator(task_id="custom_branch_task")
    custom_branch_operator >> [task_a, task_b, task_c]
