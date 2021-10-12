import sys
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import os

import scripts

sys.path.append((os.path.dirname(os.path.abspath(__file__)))+'/scripts')
from scripts import extract, load, transform

my_dag = DAG(
    dag_id= 'vaccination-data-ETL',
    start_date= days_ago(1),
    schedule_interval= '@daily'
)



Extract_data = PythonOperator(
    task_id = 'Extract_Github-OWID-vaccinations',
    python_callable= extract._extract,
    dag = my_dag
)

Transform_data = PythonOperator(
    task_id = 'Clean_aggregate_csv',
    python_callable= transform._transform,
    dag = my_dag
)

Load_data = PythonOperator(
    task_id = 'Load_Postgres',
    python_callable = load._load,
    dag = my_dag
)

print(dir(scripts))
#Extract_data >> Transform_data >> Load_data