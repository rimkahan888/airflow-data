from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable


def get_var_func():

    # Auto-deserializes a JSON value
    book_entities_var = Variable.get("book_entities", deserialize_json=True)

    # Returns the value of default_var (None) if the variable is not set
    program_name_var = Variable.get("program_name")

    print(f'Print variables, program_name {program_name_var}')
    print(f'Print variables, book_entities  {book_entities_var}')

def get_var_context_func(**context):
    return 'Print variables: '


dag = DAG(
        'alterra_get_var_examples', 
        description='Get Var Example DAG',
        schedule_interval='1 * * * *',
        start_date=datetime(2022, 10, 21), 
        catchup=False
    )

get_var = PythonOperator(
    task_id='get_var', 
    provide_context=True,
    python_callable=get_var_func, 
    dag=dag
)


# get_var_context = PythonOperator(
#     task_id='get_var_context', 
#     python_callable=get_var_context_func, 
#     dag=dag
# )

get_var 

# >> get_var_context