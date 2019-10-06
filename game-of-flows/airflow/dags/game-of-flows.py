from __future__ import print_function

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator

from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 10, 6),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}


def download_api():
    pass


with DAG("game-of-flows", default_args=default_args) as dag:
    characters_task = DataflowTemplateOperator(
        task_id='characters_task',
        template='{{var.value.buckets}}/templates/characters-pipeline',
        parameters={
        },
        dag=dag)

    character_locations_task = DataflowTemplateOperator(
        task_id='character_locations_task',
        template='{{var.value.buckets}}/templates/character-locations-pipeline',
        parameters={
        },
        dag=dag)

    download_task = PythonOperator(task_id='download_task', python_callable=download_api)

    download_task >> [characters_task] >> character_locations_task


# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(task_id="download_files", bash_command="date", dag=dag)
t2 = BashOperator(task_id="load_houses", bash_command="date", dag=dag)
t3 = BashOperator(task_id="load_characters", bash_command="date", dag=dag)
t4 = BashOperator(task_id="load_locations", bash_command="date", dag=dag)
t5 = BashOperator(task_id="load_character_locations", bash_command="date", dag=dag)


t1 >> [t2, t3, t4] >> t5
