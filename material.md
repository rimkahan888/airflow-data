# Introduction to Airflow 1	(Day-1)
## Prerequisites
- Activate docker

- Run the Airflow webserver, scheduler, database (on Postgreql) and redis locally via docker-compose.

    ```
        source docker/.env
        docker-compose -f docker/docker-compose.yaml up
    ```
- Open http://localhost:8080/home in browser, fill out credentials: `airflow/airflow`. This is how the Aiflow dashboard looks like: 

![airflow-ui](./img/airflow__ui.png)

## Apache Airflow

Apache Airflow is an open-source workflow management platform, which includes defining, executing, and monitoring workflows. 

A workflow can be defined as any sequence of steps taken to accomplish a particular goal. In an ELT pipeline, there are some workflows need to be done: 
- to move data from one or more sources to our data-warehouse (i.e: Postgresql or Citus Postgresql) and 
- to run data transformation jobs with dbt, on a scheduled manner. 


In a growing Big Data teams and more complex use cases, Airflow helps to maintain, monitor and stitch together related jobs into an end-to-end workflow.

## Concept of DAG, tasks, DAGRuns, and taskInstances, operator

Airflow works with Python

![dag-task-operator](./img/airflow__dag-task-operator.png)

- Directed Acyclic Graph (DAG)
Workflows are defined using DAGs (Directed Acyclic Graphs). in a DAG, there are composed of tasks to be executed.

    - DAGRun


- Task
    - TaskInstances

- Operators

    - EmptyOperator
    - PythonOperator
    - DbtOperator
    - AirbyteTriggerSyncOperator (https://docs.airbyte.com/operator-guides/using-the-airflow-airbyte-operator)


## Important commonly used DAG configurations 



## Create your first DAG example and check it through UI dashboard


## [TASK] TBD

# Introduction to Airflow 2	(Day-2)

## Create your first operator / implement an existing operator

## Concept of XCom, Hooks and Connection

## Implement XCom, Hooks and Connection in your DAG

## [TASK] TBD

# Review Task (Day-3)


# Schedule your data pipeline (Day-4)

## Understand how to integrate a data pipeline into airflow scheduling

https://www.freecodecamp.org/news/orchestrate-an-etl-data-pipeline-with-apache-airflow/

Setup a DAG script
- Prepare the dataset (some CSV files or URL)
- Create DAG to ingest the dataset to our datawarehouse with python
    1. define when the DAG will be run, start_date
    2. define the interval of the DAG
- Setup Postgresql DB Connection
- Define tasks in a DAG : 
    1. task-1: define empty operator
    2. task-2: create connection and table in postgresql with PostgresOperator
    3. task-3: ingest data from file with PythonOperator
    4. task-4: command to move data from Postgresql to Citus with Airbyte
    5. task-5: dbt command to transform data with DbtOperator, BashOperator or SSHOperator
- Create dependencies between tasks
- Test the workflows

## Scheduling ingestion code with PythonOperator

## Scheduling dbt code with BashOperator

## Send success/failed notification to email

## [TASK] TBD