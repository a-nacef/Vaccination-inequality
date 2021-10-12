import sys
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
sys.path.append('/home/aziz/airflow/dags/vax-dbrd')
import os
import etlscripts

my_dag = DAG(
    dag_id= 'vaccination-data-ETL',
    start_date= days_ago(1),
    schedule_interval= '@daily'
)


Extract_data = PythonOperator(
    task_id = 'Extract_Github-OWID-vaccinations',
    python_callable= etlscripts._extract,
    dag = my_dag
)

Transform_data = PythonOperator(
    task_id = 'Clean_aggregate_csv',
    python_callable= etlscripts._transform,
    dag = my_dag
)

Load_data = PythonOperator(
    task_id = 'Load_Postgres',
    python_callable = etlscripts._load,
    dag = my_dag
)

Extract_data >> Transform_data >> Load_data