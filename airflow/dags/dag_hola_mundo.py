from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def saludar():
    print("Hola desde Airflow 🌀")

with DAG(
    dag_id="dag_hola_mundo",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@once",
    catchup=False
) as dag:
    tarea = PythonOperator(
        task_id="saludo",
        python_callable=saludar
    )
