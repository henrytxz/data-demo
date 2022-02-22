"""
this example dag shows 1 to many then many to 1 dependency.

     t1
   /    \
 t0       t3
   \    /
     t2

t0 (task 0) triggers both t1 and t2 (1 to many relationship)
t3 runs after both t1 AND t2 are done (many to 1 relationship)
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'data_engineering',
}

def business_logic(x):
    """
    right now this has the simplest logic but in theory you could put as much business logic here as you like,
    as long as it's elegant :)
    """
    return x

with DAG(
    dag_id='one_to_many_to_one',
    default_args=args,
    schedule_interval="@once",
    start_date=days_ago(1),
) as dag:

    # maybe not everyone uses Python: here a for loop that creates 4 very similar tasks and append them to a list
    tasks = []
    for i in range(4):
        tasks.append(
            PythonOperator(
                task_id=f't{i}',
                python_callable=business_logic,
                op_kwargs={'x': i}
            )
        )

    """
    the next 2 lines specify this directed acyclic graph (dag)
    dag goes from left to right
    this little graph doesn't have arrows but it's directed => going from left to right ONLY
    since it is directed, this does not form a cycle.
    
    it's important there is no cycle because a cycle would mean a dag never, ever finishing.
    
         t1
       /    \
     t0       t3
       \    /
         t2
    """
    tasks[0] >> tasks[1] >> tasks[3]
    tasks[0] >> tasks[2] >> tasks[3]
