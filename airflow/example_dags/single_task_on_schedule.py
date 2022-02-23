"""
this example dag shows how Airflow supports scheduling.

Airflow schedule interval uses cron,
for more details, see https://airflow.apache.org/docs/apache-airflow/1.10.10/scheduler.html

in this dag, @hourly was used but Airflow also supports other cron presets (all can be found at the link above)
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
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
    dag_id='run_a_task_on_schedule',
    default_args=args,
    schedule_interval="@hourly",
    start_date=days_ago(1),
    max_active_runs=1,
) as dag:

    t1 = PythonOperator(
        task_id='a_simple_task',
        python_callable=do_work,
        op_kwargs={'x': 1},
    )