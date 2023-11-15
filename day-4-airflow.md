
# [Day-4] Schedule an End-to-End Data Pipeline

## Scheduling dbt code with DockerOperator

## Send success/failed notification to email
- setup google App passwords https://security.google.com/settings/security/apppasswords 
- setup SMTP config on airflow.cfg or in docker-compose common
- register for smtp server https://stackoverflow.com/questions/51829200/how-to-set-up-airflow-send-email, https://hevodata.com/learn/airflow-emailoperator/
- create .env file to store credentials data
- run docker and load .env

```
docker-compose -f docker/docker-compose.yaml --env-file docker/.env up
```

## [TASK] TBD