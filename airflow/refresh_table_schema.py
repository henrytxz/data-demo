from datetime import timedelta

from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import \
	BigQueryDeleteTableOperator, BigQueryCreateEmptyTableOperator
from airflow.utils.dates import days_ago

default_args = {
	'owner': 'data_engineering',
	'email_on_failure': True,
	'email_on_retry': False,
	'email': ['demo@demo.com'],
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}

BUCKET = 'us-east1-demo-e11d66ca-bucket'

with DAG(
		dag_id='create_replace_game_play_activity_table',
		default_args=default_args,
		start_date=days_ago(1),
		max_active_runs=1,
		schedule_interval='@once'
) as dag:

	drop = BigQueryDeleteTableOperator(
		task_id=f'drop_table_if_already_exists',
		deletion_dataset_table='henrytxz.data_demo.game_play_activity',
		gcp_conn_id='google_cloud_default',
		ignore_if_missing=True
	)

	create = BigQueryCreateEmptyTableOperator(
		task_id=f'create_table',
		project_id='henrytxz',
		dataset_id='data_demo',
		table_id='game_play_activity',
		gcs_schema_object=f'gs://{BUCKET}/dags/airflow/game_play_activity.json',
		bigquery_conn_id='google_cloud_default',
		google_cloud_storage_conn_id='google_cloud_default',
		exists_ok=True
	)

	drop >> create
