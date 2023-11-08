from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

with DAG(
    'alterra_xcom_examples_without_decorator', 
    description='Print xcom Example DAG',
    schedule_interval=None,
    start_date=datetime(2022, 10, 21), 
    catchup=False
) as dag:
    # ti = task instance
    def push_var_from_task_a(ti=None):
        ti.xcom_push(key='book_title', value='Data Engineering 101')
    
    def get_var_from_task_a(ti=None):
        book_title = ti.xcom_pull(task_ids='push_var_from_task_a', key='book_title')
        print(f'print book_title variable from xcom: {book_title}')

    push_var_from_task_a_task = PythonOperator(
        task_id = 'push_var_from_task_a',
        python_callable = push_var_from_task_a
    )

    get_var_from_task_a_task = PythonOperator(
        task_id = 'get_var_from_task_a',
        python_callable = get_var_from_task_a
    )

    push_var_from_task_a_task >> get_var_from_task_a_task