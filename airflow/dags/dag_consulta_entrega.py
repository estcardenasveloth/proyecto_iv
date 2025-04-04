from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sqlite3

# Ruta del archivo SQL y base de datos montados en el contenedor
SQL_FILE = '/opt/airflow/queries/delivery_date_difference.sql'
DB_PATH = '/opt/airflow/olist.db'

def ejecutar_consulta():
    # Leer el contenido de la consulta SQL
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        sql = f.read()

    # Conectar a la base de datos y ejecutar la consulta
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql)

    resultados = cur.fetchall()
    print("Resultados:")
    for fila in resultados:
        print(fila)

    cur.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='consulta_diferencia_entrega',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    tarea_sql = PythonOperator(
        task_id='ejecutar_consulta_sqlite',
        python_callable=ejecutar_consulta
    )

    tarea_sql
