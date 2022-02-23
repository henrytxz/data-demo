from airflow import DAG
from airflow.providers.google.cloud.operators.kubernetes_engine import GKEStartPodOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago

args = {
    'owner': 'data_engineering',
}

GCP_PROJECT_ID = "henrytxz"
GCP_LOCATION   = "us-east1"
CLUSTER_NAME   = "us-east1-demo-f5cd9848-gke"
DBT_IMAGE      = "us-docker.pkg.dev/henrytxz/data-demo/data-demo-docker-workload:latest"

with DAG(
    dag_id='docker_workload',
    default_args=args,
    schedule_interval='@hourly',
    start_date=days_ago(1),
    tags=['data-demo'],
) as dag:

    sensor = ExternalTaskSensor(
        task_id='external_task_sensor',
        external_dag_id='sql_workload',
        poke_interval=30,
        check_existence=True
    )

    docker_task = GKEStartPodOperator(
        task_id='docker_task',
        project_id=GCP_PROJECT_ID,
        location=GCP_LOCATION,
        cluster_name=CLUSTER_NAME,
        do_xcom_push=False,
        namespace='default',
        image=DBT_IMAGE,
        name='docker_task',
        is_delete_operator_pod=True,
        startup_timeout_seconds=60*5,
    )

    sensor >> docker_task