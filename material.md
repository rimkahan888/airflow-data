# Introduction to Airflow 1	(Day-1)
## Prerequisites
- Activate docker
- Install Airflow, Postgresql and Redis locally
    ```
        source docker/.env
        docker-compose -f docker/docker-compose.yaml up
    ```
- Open http://localhost:8080/home in browser, fill out credentials: `airflow/airflow`

## Concept of DAG, tasks, DAGRuns, and taskInstances, operator


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

## Scheduling ingestion code with PythonOperator

## Scheduling dbt code with BashOperator

## Send success/failed notification to email

## [TASK] TBD