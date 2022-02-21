from datetime import timedelta

from airflow import DAG
from airflow.providers.google.cloud.operators.kubernetes_engine import GKEStartPodOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

GCP_PROJECT_ID = "henrytxz"
GCP_LOCATION   = "us-east1"
CLUSTER_NAME   = "us-east1-demo-f5cd9848-gke"
DBT_IMAGE      = "us-docker.pkg.dev/henrytxz/data-demo/data-demo-dbt:latest"

with DAG(
    dag_id='SQL_workload',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
) as dag:

    dbt_run = GKEStartPodOperator(
        task_id='dbt_build',
        project_id=GCP_PROJECT_ID,
        location=GCP_LOCATION,
        cluster_name=CLUSTER_NAME,
        do_xcom_push=False,
        namespace='default',
        image=DBT_IMAGE,
        cmds=["dbt", "build", "--profile", "dev"],
        # cmds=["dbt", "build", "--profile", "prod"],
        name='dbt_build',
        is_delete_operator_pod=True,
        startup_timeout_seconds=60*5,
        env_vars={'PATH_GCP_KEYFILE': '/dbt/dbt-user.json'}
    )
