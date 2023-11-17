
# [Day-3] Schedule an End-to-End Data Pipeline

In this section, we are going to implement scheduling for our ETL pipeline that we have learned.


## Understand how to integrate a data pipeline into airflow

https://www.freecodecamp.org/news/orchestrate-an-etl-data-pipeline-with-apache-airflow/

[DONE]
Setup a DAG script
- Prepare the dataset (some CSV files or URL)
- Create code to ingest the dataset to our datawarehouse with python
    1. define when the DAG will be run, start_date
    2. define the interval of the DAG
- Setup Postgresql DB Connection
- Define tasks in a DAG : 
    1. task-1: define empty operator
    2. task-2: create connection and table in postgresql with PostgresOperator
    3. task-3: ingest data from file with PythonOperator

[TODO] 
    4. task-5: dbt command to transform data with BashOperator
    5. task-6: send notification to email
- Create dependencies between tasks
- Test the workflows



### Setup dbt in a Dockerfile

- dbt in [Dockerfile](./docker/Dockerfile)

- to setup dbt directory on local machine, review material about [dbt](https://github.com/Immersive-DataEngineer-Resource/dbt-demo).

```
python -m venv .venv
source .venv/bin/activate
pip install dbt-postgres # Note: DBT has many DBMS adapter

```
- initiate a dbt project

```
dbt init transformation

```
- setup profiles.yml

```
mkdir transformation/profiles
touch transformation/profiles/profiles.yml
```

- fill this to profiles.yml

```

transformation:
  outputs:

    dev:
      type: postgres
      threads: 1
      host: host.docker.internal
      port: 5432
      user: airflow
      pass: airflow
      dbname: airflow
      schema: public

  target: dev


```

- create a file named dbt.env to store environment variable for DBT

```
export DBT_PROFILES_DIR=$(pwd)/dbt-profiles
```

- run dbt debug command

```
dbt debug --project-dir ./transformation
```



