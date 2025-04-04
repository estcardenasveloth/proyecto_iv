from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append("/opt/airflow/src")

from extract import extract
from transform import run_queries
from load import load

from sqlalchemy import create_engine

CSV_FOLDER = "/opt/airflow/datasetdocker compose"
PUBLIC_HOLIDAYS_URL = "https://date.nager.at/api/v3/PublicHolidays"
CSV_TABLE_MAPPING = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_translation",
}

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

def ejecutar_etl_completo():
    engine = create_engine("sqlite:////opt/airflow/olist.db")

    print("▶ Extrayendo datos...")
    dataframes = extract(CSV_FOLDER, CSV_TABLE_MAPPING, PUBLIC_HOLIDAYS_URL)

    print("▶ Cargando datos...")
    load(dataframes, engine)

    print("▶ Transformando datos...")
    resultados = run_queries(engine)

    for nombre, df in resultados.items():
        print(f"\n>>> {nombre} ({df.shape[0]} filas)")
        print(df.head(3).to_string(index=False))

with DAG(
    dag_id="etl_olist_completo",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@once",
    catchup=False,
) as dag:

    ejecutar_todo = PythonOperator(
        task_id="ejecutar_etl_completo",
        python_callable=ejecutar_etl_completo,
    )
