from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def get_var_func():
    return 'Print variables: '

def get_var_context_func(**context):
    return 'Print variables: '


dag = DAG(
        'get_var_examples', 
        description='Get Var Example DAG',
        schedule_interval='* * * * *',
        start_date=datetime(2022, 10, 21), 
        catchup=False
    )

get_var = PythonOperator(
    task_id='get_var', 
    python_callable=get_var_func, 
    dag=dag
)

get_var_context = PythonOperator(
    task_id='get_var_context', 
    python_callable=get_var_context_func, 
    dag=dag
)

get_var >> get_var_context