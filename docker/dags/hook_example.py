from airflow import DAG
from datetime import datetime
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator

with DAG(
    dag_id = 'alterra_hook_example',
    schedule=None,
    start_date=datetime(2022, 10, 21),
    catchup=False
) as dag:

    create_table_in_db_task = PostgresOperator(
        task_id = 'create_table_in_db',
        sql = ('CREATE TABLE IF NOT EXISTS yellow_tripdata ' +
        '(' +
            'vendor_id BIGINT, ' +
            'tpep_pickup_datetime TIMESTAMP WITHOUT TIME ZONE, ' +
            'tpep_dropoff_datetime TIMESTAMP WITHOUT TIME ZONE, ' +
            'passenger_count BIGINT, ' +
            'trip_distance FLOAT(53), ' +
            'ratecode_id BIGINT, ' +
            'store_and_fwd_flag TEXT, ' +
            'pu_location_id BIGINT, ' +
            'do_location_id BIGINT, ' +
            'payment_type BIGINT, ' +
            'fare_amount FLOAT(53), ' +
            'extra FLOAT(53), ' +
            'mta_tax FLOAT(53), ' +
            'tip_amount FLOAT(53), ' +
            'tolls_amount FLOAT(53), ' +
            'improvement_surcharge FLOAT(53), ' +
            'total_amount FLOAT(53), ' +
            'congestion_surcharge FLOAT(53) ' +
        ')'),
        postgres_conn_id='pg_conn_id', 
        autocommit=True,
        dag=dag
    )

    def loadDataToPostgres():
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id').get_conn()
        curr = pg_hook.cursor("cursor")
        with open('/opt/airflow/dags/sample.csv', 'r') as file:
            next(file)
            curr.copy_from(file, 'yellow_tripdata', sep=',')
            pg_hook.commit()


    load_data_to_db_task = PythonOperator(
        task_id='load_data_to_db',
        python_callable=loadDataToPostgres,
        dag=dag
    )


    create_table_in_db_task >> load_data_to_db_task