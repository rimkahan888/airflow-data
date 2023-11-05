from datetime import datetime
from airflow import DAG
from operators.hello_operator import HelloWorldOperator

dag = DAG(
        'alterra_hello_world_with_operator',
        schedule_interval='@once',
        start_date=datetime(2022, 10, 21), 
        catchup=False
    )

custom_operator_hello_task = HelloWorldOperator(
    param1='This is an example operator by', 
    param2='alterra-student',
    task_id='hello_world_task', 
    dag=dag
)

custom_operator_hello_task