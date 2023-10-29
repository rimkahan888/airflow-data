# Introduction to Airflow 1	(Day-1)
## Prerequisites
- Activate docker
- An Airflow instance is composed of a scheduler, an executor, a webserver, and a metadata database. Run the Airflow instance locally via docker-compose.

    ```
        source docker/.env
        docker-compose -f docker/docker-compose.yaml up
    ```
- Open http://localhost:8080/home in browser, fill out credentials: `airflow/airflow`. This is how the Aiflow dashboard looks like: 

![airflow-ui](./img/airflow__ui.png)

## Apache Airflow

Apache Airflow is an open-source workflow management platform, which includes defining, executing, and monitoring workflows. Workflows are defined using `DAGs` (Directed Acyclic Graphs). In a DAG, there are a set of `Tasks` to be executed.

In growing Big Data use cases, Airflow helps to maintain, monitor and stitch together more complex and depending jobs into an end-to-end workflow.

## Concept of DAG, Task, and Operator

![dag-task-operator](./img/airflow__dag-task-operator.png)

- Directed Acyclic Graph (DAG)


    In Airflow, a workflow is defined as a DAG (Directed Acyclic Graph) that contains individual units of work called Tasks. In simple terms, a DAG is a graph with nodes connected via directed edges. Also, there should be no cycles within such a graph. 

    Suppose in an ELT pipeline, we define a DAG contains some Tasks, such as: 
    - extract data from one or more sources 
    - load data to our data-warehouse
    - run data transformation
    - send email notification when error happens

    ![airflow-dag-tasks](./img/airflow__dag_task.png)

    Whenever a DAG is triggered a DAGRun is created, so a DAGRun is an instance of the DAG with an execution timestamp. 

- Operator
    Operator is a template or class for performing a specific task. If we want to execute a Python script, we need a `PythonOperator`. If we want to execute Bash command, we need `BashOperator`. There are [built-in operators](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/index.html), such as: `EmailOperator`, `EmptyOperator`, etc.

    We can also install more operators from [Provider packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html) to further extend Airflow’s functionalities.


- Task
    A task is an instantiation of an operator and simply can be thought of as a unit of work that is represented as a node in a DAG.

    Whenever a Task is running, a task instance is created. A task instance belongs to DAGRuns, has an associated `execution_date`. Task instances go through various states, such as “running,” “success,” “failed,” “skipped,” “retry,” etc. Each task instance (and task) has a life cycle through which it moves from one state to another.

## Create our first DAG on Airflow 

- We are going to create our first DAG that will print a 'hello world' message to the log. The code can be found [here](./docker/dags/hello_world.py). The [DAG code](./docker/dags/hello_world.py) is placed on our AIRFLOW_HOME directory under the dags folder.

![airflow-dag-folder](./img/airflow__dag_folder.png)


- Let's understand the code. In the first few lines, we are simply importing a few packages from airflow.

    ```
        from datetime import datetime
        from airflow import DAG
        from airflow.operators.python_operator import PythonOperator

    ```

- Then, we define a Python function that will print the hello message.

    ```
        def print_hello():
            return 'Hello world from first Airflow DAG!'
    ```

- We declare the DAG arguments, such as: `name`, `description`, `schedule_interval`, `start_date` and `catchup`. 
    - `schedule_interval` means the interval of time from the minimum `start_date` at which we want our DAG to be triggered. The value can be `None`,`@once`,`@hourly`,`@daily`,`@weekly`,`@monthly`,`@yearly` or the Cron expression (see guide in [crontab.guru](https://crontab.guru/)).
    - `start_date` means the date at which DAG will start being scheduled.
    - `catchup=False` setting to prevent Airflow from having the DAG runs any past scheduled intervals that have not been run (backfill). By default, the `catchup` value is `True`.

    ```
        dag = DAG(
                'hello_world', 
                description='Hello World DAG',
                schedule_interval='* * * * *',
                start_date=datetime(2022, 10, 21), 
                catchup=False
            )
    ```

- Next, we define the task and call it the `hello_operator` task. The task uses the in-built `PythonOperator` to call our `print_hello` function. We also provide a `task_id` to this task.

    ```
        operator_hello_world = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)
    ```

- The last statement specifies the order of the task. In this case, we have only one task, no upstream or downstream task.
    ```
        operator_hello_world
    ```

- Let's check it through Airflow dashboard. Find the name defined for our DAG `hello_world` on the list of DAGs.

![airflow-activate-dag](./img/airflow_activate_the_dag.png)

- Click on the `hello_world` DAG, then we will be going through the detail page that shows a sequence of green-squared status meaning the DAG runs succesfully in a scheduled interval.

![airflow-graph-run](./img/airflow_graph_run.png)

- Click on the green-squared status, then click on the tab `Logs` to see the log of the DAG.

![airflow-log](./img/airflow_logs.png)

## TASK

1. [TBD] Create DAG that will run in every 3 hours.
2. [TBD] Create the upstream task and downstream task.

# Introduction to Airflow 2	(Day-2)

## Create your First Operator

Now we’ll create our own operator that extends previous HelloWorld example, we’ll call the HelloWorldOperator. It will print a message on the console with the argument passed into it. The code can be found here: 
- [Operator code](./docker/plugins/operators/hello_operator.py)
- [DAG code](./docker/dags/hello_world_operator.py)

- Let's go through the [operator code](./docker/plugins/operators/hello_operator.py). First, create a sub directory `operators` under `plugins`. Then, create a file named `hello_operator.py`. 

- All operators are derived from the `BaseOperator` class. The code for our `HelloWorldOperator` appears below.

```
class HelloWorldOperator(BaseOperator):
    def __init__(self, param1, param2, *args, **kwargs) -> None:
        self.param1 = param1
        self.param2 = param2
        super(HelloWorldOperator, self).__init__(*args, **kwargs)


```

- The line that contains `super` function is used to refer to the `BaseOperator` class or `HelloWorldOperator`

- The main logic of our operator is in the `execute` method. The `HelloWorldOperator` will simply print a message to a console.

```
    def execute(self, context):
        print(f'Hello World from Operator: {self.param1} {self.param2}')
```

- Now, we can import our custom operator to the DAG. Let's runthrough to our [DAG code](./docker/dags/hello_world_operator.py).

- The DAG declaration is similar with the previous example. We will use our custom `HelloWorldOperator` operator to print message to the console. Operator helps us to avoid repetition function.

```
    custom_operator_hello_task = HelloWorldOperator(
        param1='This is an example operator by', 
        param2='alterra-student',
        task_id='hello_world_task', 
        dag=dag
    )

```

- Next, specify the order of the task.

```
    custom_operator_hello_task
```

## Define Variables, XCom, Hooks, Connection 

- Variables 

Variables in Airflow are a key-value store contains settings that can be queried from our tasks and can be set via Airflow dashboard or imported as a JSON file.

```

```

![airflow-variables](./img/airflow__variables.png)

- XCom (cross-communication)

XCom in Airflow is the way to pass data from one `Task`/`Operator` to another. The data to be shared is stored in the database with an associated execution date, task instance, and DAG run by the sending task and then retrieved from the database by the intended recipient task. 

To send and retrieve objects we can use method: `xcom_push()` and `xcom_pull()`.

- Hooks

- Connection
≥,mn m,./0p980-p8-pl []

# Review Task (Day-3)


# Schedule your data pipeline (Day-4)

In this section, we are going to implement scheduling for our ETL pipeline that we have learned.

## Understand how to integrate a data pipeline into airflow

https://www.freecodecamp.org/news/orchestrate-an-etl-data-pipeline-with-apache-airflow/

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
    4. task-4: command to move data from Postgresql to Citus with Airbyte
    5. task-5: dbt command to transform data with DbtOperator, BashOperator or SSHOperator
- Create dependencies between tasks
- Test the workflows

## Scheduling ingestion code with PythonOperator

## Scheduling dbt code with BashOperator

## Send success/failed notification to email

## [TASK] TBD