from datetime import timedelta

from airflow import DAG
from airflow.kubernetes.secret import Secret
from airflow.providers.google.cloud.operators.kubernetes_engine import GKEStartPodOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'data_engineering',
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

# followed https://cloud.google.com/composer/docs/composer-2/use-kubernetes-pod-operator#secret-config
# This secret was created in the GKE cluster by doing the following at Google Cloud Shell:
# kubectl create secret generic dbt-user-key --from-file dbt-user.json=./dbt-user.json
# kubectl create secret SECRET_TYPE SECRET_NAME --from-file key=PATH_TO_FILE1
# the following would deploy the secret to /dbt/secrets/dbt-user.json in the pod started by GKEStartPodOperator
secret_volume = Secret(
    deploy_type='volume',
    deploy_target='/dbt/secrets',   # Path where we mount the secret as volume. Do not use an existing path, that will replace content of that folder.
    secret='dbt-user-key',          # Name of Kubernetes Secret
    key='dbt-user.json')            # Key in the form of service account file name

with DAG(
    dag_id='SQL_workload',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
) as dag:

    dbt_build = GKEStartPodOperator(
        task_id='dbt_build',
        project_id=GCP_PROJECT_ID,
        location=GCP_LOCATION,
        cluster_name=CLUSTER_NAME,
        do_xcom_push=False,
        namespace='default',
        image=DBT_IMAGE,
        cmds=["dbt", "build", "--profile", "prod"],
        name='dbt_build',
        is_delete_operator_pod=True,
        startup_timeout_seconds=60*5,
        secrets=[secret_volume],
        env_vars={'PATH_GCP_KEYFILE': '/dbt/secrets/dbt-user.json'}
    )
