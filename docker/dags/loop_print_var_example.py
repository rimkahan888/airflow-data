from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

with DAG(
    'alterra_loop_print_var_examples', 
    description='Loop Print Variables Example DAG',
    schedule_interval=None,
    start_date=datetime(2022, 10, 21), 
    catchup=False
) as dag:
    def print_var(**kwargs):
        print(f'Print variables from kwargs {kwargs["task"]}')

    looping_tasks_var = Variable.get("looping_task", deserialize_json=True)["task_name"]
    for task_name in looping_tasks_var:
        PythonOperator(
            task_id=f'loop_var_{task_name}',
            python_callable=print_var,
            op_kwargs={
                "task": task_name
            }
        )