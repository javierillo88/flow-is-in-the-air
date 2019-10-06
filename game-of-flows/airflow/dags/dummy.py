from __future__ import print_function

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

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


def conquer_the_north():
    print('The North has been defeated')


def conquer_the_vale():
    print('The Mountain and the Vale has been defeated')


def conquer_the_rock():
    print('The Rock has been defeated')


def conquer_the_rivers():
    print('The Isles and the Rivers has been defeated')


def conquer_the_rock():
    print('The Rock has been defeated')


def conquer_the_stormlands():
    print('The Stormlands has been defeated')


def conquer_the_reach():
    print('The Reach, has been defeated')


def rule_the_seven_kingdoms():
    print('Congrats Aegon, rule of all them!')


with DAG("dummy-game-of-flows", default_args=default_args) as dag:

    conquer_the_north_task = PythonOperator(task_id='conquer_the_north_task', python_callable=conquer_the_north)
    conquer_the_vale_task = PythonOperator(task_id='conquer_the_vale_task', python_callable=conquer_the_vale)
    conquer_the_rivers_task = PythonOperator(task_id='conquer_the_rivers_task', python_callable=conquer_the_rivers)
    conquer_the_rock_task = PythonOperator(task_id='conquer_the_rock_task', python_callable=conquer_the_rock)
    conquer_the_stormlands_task = PythonOperator(task_id='conquer_the_stormlands_task', python_callable=conquer_the_stormlands)
    conquer_the_reach_task = PythonOperator(task_id='conquer_the_reach_task', python_callable=conquer_the_reach)

    rule_the_seven_kingdoms_task = PythonOperator(task_id='rule_the_seven_kingdoms_task', python_callable=rule_the_seven_kingdoms)

    (conquer_the_stormlands_task >> [conquer_the_rock_task, conquer_the_reach_task]
     >> conquer_the_rivers_task >> [conquer_the_vale_task, conquer_the_north_task]
     >> rule_the_seven_kingdoms_task)

