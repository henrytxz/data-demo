from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago

args = {
    'owner': 'data_engineering',
}

def do_work(x):
    """
    the business logic you put here will be run inside a Python process.
    suppose you decide do_work should double the keyword argument x and return.
    """
    return x * 2

with DAG(
    dag_id='python_workload',
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

    python_task = PythonOperator(
        task_id='python_task',
        python_callable=do_work,
        op_kwargs={'x': 1},
    )

    sensor >> python_task