from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import random

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'postgres_sample_etl',
    default_args=default_args,
    description='A sample ETL process with PostgreSQL',
    schedule_interval=timedelta(days=1),
)

def generate_sample_data():
    data = []
    for i in range(10):
        data.append({
            'user_id': i,
            'username': f'user_{i}',
            'score': random.randint(1, 100)
        })
    return data

def load_data_to_postgres():
    data = generate_sample_data()
    df = pd.DataFrame(data)
    
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO user_scores (user_id, username, score) VALUES (%s, %s, %s)",
            (row['user_id'], row['username'], row['score'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_default',
    sql="""
        CREATE TABLE IF NOT EXISTS user_scores (
            user_id INTEGER PRIMARY KEY,
            username VARCHAR(50),
            score INTEGER
        );
    """,
    dag=dag
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_postgres,
    dag=dag
)

create_table >> load_data

"""
DAG Description:
---------------
This DAG does the following:
1. Creates a table called user_scores in PostgreSQL if it doesn't exist
2. Generates sample user data with random scores
3. Loads the generated data into the PostgreSQL database

Setup Requirements:
-----------------
Before running this DAG, you need to:

1. Install required dependencies:
   pip install apache-airflow-providers-postgres pandas

2. Configure PostgreSQL connection in Airflow:
   - Go to the Airflow UI
   - Navigate to Admin → Connections
   - Add a new connection with:
     - Conn Id: postgres_default
     - Conn Type: Postgres
     - Host: your_postgres_host
     - Schema: your_database_name
     - Login: your_username
     - Password: your_password
     - Port: 5432

Note: The DAG will run daily and insert 10 random user records into the PostgreSQL database.
You can modify the schedule_interval and the number of records generated according to your needs.
"""