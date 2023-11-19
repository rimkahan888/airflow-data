from airflow import DAG
from datetime import datetime
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash import BashOperator
from docker.types import Mount
from airflow.operators.email_operator import EmailOperator

default_args = {'owner' : 'airflow'}

with DAG(
    dag_id = 'alterra_integrate_all_part2',
    default_args=default_args,
    schedule=None,
    start_date=datetime(2022, 10, 21),
    catchup=False
) as dag:

    start = DummyOperator(task_id="start")

    create_table_in_db_task = PostgresOperator(
        task_id = 'create_table_in_db',
        sql = ('CREATE TABLE IF NOT EXISTS github_data ' +
        '(' +
            'id BIGINT, ' +
            'type TEXT, ' +
            'actor JSON, ' +
            'repo JSON, ' +
            'payload JSON, ' +
            'public TEXT, ' +
            'created_at  TIMESTAMP WITHOUT TIME ZONE, ' +
            'org JSON ' +
        ')'),
        postgres_conn_id='pg_conn_id', 
        autocommit=True,
        dag=dag
    )

    # extract data from url (gz), based on execution date (1 hari)
    def extract():
        import pandas as pd
        import json

        """The main ETL function"""
        year = 2020
        month = 1
        day = 1
        hour = 1
        dataset_file = f"{year}-{month:02}-{day:02}-{hour}"
        print(f"hour:{hour}, file:{dataset_file}")
        dataset_url = f"https://data.gharchive.org/{year}-{month:02}-{day:02}-{hour}.json.gz"

        header = {'User-Agent': 'pandas'}

        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        engine = pg_hook.get_sqlalchemy_engine()

        # chunk_size = int(kwargs["CHUNK_SIZE"])
        chunk_size = 5000
        with pd.read_json(dataset_url, lines=True, storage_options=header, chunksize=chunk_size, compression="gzip") as reader: 
            reader
            print(">>>> store data")
            for chunk in reader:
                df = pd.DataFrame(chunk)
                
                df.dropna(inplace=True)

                df["id"] = df["id"].astype("Int64")
                df["type"] = df["type"].astype("string")
                df["public"] = df["public"].astype("string")
                df["created_at"] = pd.to_datetime(df["created_at"])

                df["actor"] = df["actor"].apply(lambda x: json.dumps(x)).astype("string")
                df["repo"] = df["repo"].apply(lambda x: json.dumps(x)).astype("string")
                df["payload"] = df["payload"].apply(lambda x: json.dumps(x)).astype("string")
                df["org"] = df["org"].apply(lambda x: json.dumps(x)).astype("string")

                df.to_sql("github_data", con=engine, if_exists="append", index=False, schema="public", method=None, chunksize=5000)

    load_data_to_db_task = PythonOperator(
        task_id='load_data_to_db',
        python_callable=extract,
        op_kwargs=None,
        dag=dag
    )

    # remove duplication with dbt, run models with dbt

    local_path = "/Users/dewi.oktaviani/Documents/personal-github/airflow-data/docker"
    
    dbt_debug_cmd = DockerOperator(
        task_id='dbt_debug_cmd',
        image='dbt_in_docker_compose',
        container_name='dbt_container',
        api_version='auto',
        auto_remove=True,
        command="bash -c 'dbt debug'",
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        mounts = [
            Mount(
                source=f"{local_path}/transformation", 
                target="/usr/app", 
                type="bind"
            ),
            Mount(
                source=f"{local_path}/transformation/profiles",
                target="/root/.dbt",
                type="bind"
            )
        ],
        mount_tmp_dir = False
    )

    dbt_run_cmd = DockerOperator(
        task_id='dbt_run_cmd',
        image='dbt_in_docker_compose',
        container_name='dbt_container',
        api_version='auto',
        auto_remove=True,
        command="bash -c 'dbt --no-partial-parse run'",
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        mounts = [
            Mount(
                source=f"{local_path}/transformation", 
                target="/usr/app", 
                type="bind"
            ),
            Mount(
                source=f"{local_path}/transformation/profiles",
                target="/root/.dbt",
                type="bind"
            )
        ],
        mount_tmp_dir = False
    )

    # NEXT
    # part-3: send notif to email

    end = DummyOperator(task_id="end")


    start >> create_table_in_db_task >> load_data_to_db_task >> dbt_debug_cmd >> dbt_run_cmd >> end 