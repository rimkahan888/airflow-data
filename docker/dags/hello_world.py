from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def print_hello():
    return 'Hello world from first Airflow DAG!'

dag = DAG(
        'alterra_hello_world', 
        description='Hello World DAG',
        schedule_interval='* * * * *',
        start_date=datetime(2022, 10, 21), 
        catchup=False
    )

operator_hello_world = PythonOperator(
    task_id='hello_task', 
    python_callable=print_hello, 
    dag=dag
)

operator_hello_world