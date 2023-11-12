from airflow import DAG
from datetime import datetime
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator

with DAG(
    dag_id = 'alterra_integrate_all',
    schedule=None,
    start_date=datetime(2022, 10, 21),
    catchup=False
) as dag:

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

    # extract data from url (gz)
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

        # for key, value in kwargs.items():
        #     print("%s == %s" % (key, value))
        
        header = {'User-Agent': 'pandas'}

        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        engine = pg_hook.get_sqlalchemy_engine()

        df_schema = {}

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

                df.to_sql("github_data", con=engine, if_exists="append", index=False, schema="public", dtype=df_schema, method=None, chunksize=5000)

    load_data_to_db_task = PythonOperator(
        task_id='load_data_to_db',
        python_callable=extract,
        op_kwargs=None,
        dag=dag
    )


    create_table_in_db_task >> load_data_to_db_task