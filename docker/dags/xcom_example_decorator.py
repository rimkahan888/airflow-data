from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

with DAG(
    'alterra_xcom_examples_with_decorator', 
    description='Print xcom Example DAG',
    schedule_interval='1 * * * *',
    start_date=datetime(2022, 10, 21), 
    catchup=False
) as dag:
    # ti = task instance
    # The @task decorator is recommended over the classic PythonOperator to execute Python callables.
    @task
    def push_var_from_task_a(ti=None):
        ti.xcom_push(key='book_title', value='Data Engineering 101')
    
    @task
    def get_var_from_task_a(ti=None):
        book_title = ti.xcom_pull(task_ids='push_var_from_task_a', key='book_title')
        print(f'print book_title variable from xcom: {book_title}')

    push_var_from_task_a() >> get_var_from_task_a()