from datetime import datetime
from airflow import DAG
from docker.types import Mount
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

CONN_ID = '6504b8fd-e29e-4fb0-aa7e-d1e6314fc42e'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'elt_and_dbt_with_airbyte',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime.today(),
    catchup=False
)

task1 = AirbyteTriggerSyncOperator(
    task_id='airbyte_postgres_postgres',
    airbyte_conn_id='airbyte',
    connection_id=CONN_ID,
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag
)

task2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',    # same as docker compose dbt image
    command=[
        'run',
        '--profiles-dir',
        '/root',
        '--project-dir',
        '/opt/dbt'
    ],
    auto_remove=True,
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    mounts=[
        Mount(source='/mnt/c/Users/allen/Documents/Code/Data Engineering/Intro/ELT/custom_postgres',
              target='/opt/dbt', type='bind'),
        Mount(source='/home/alsiu/.dbt',
              target='/root', type='bind')
    ],
    dag=dag
)

task1 >> task2
