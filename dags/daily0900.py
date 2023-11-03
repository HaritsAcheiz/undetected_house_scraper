from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from includes.ARTrans import ARTrans

default_args = {
    'owner': 'Harits',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 11, 3),
    'email': ['harits.muhammad.only@gmail.com'],
    'catchup': False,
    # 'depends_on_past': False,
    'email_on_failure': False
    # 'email_on_retry': False,
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

@dag(dag_id='daily0900',
     catchup=False,
     schedule='@daily',
     default_args=default_args,
     )

def daily0900():

    scrape_link = BashOperator(task_id='scrape_link',
                               bash_command="python /opt/airflow/dags/includes/scrape_link.py")

    scrape_link

daily0900()