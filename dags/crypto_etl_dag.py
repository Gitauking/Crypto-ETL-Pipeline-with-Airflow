from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2

default_args = {
    'owner': 'gitau',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def extract():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data

def transform(data):
    return {
        'bitcoin_price': data['bitcoin']['usd'],
        'ethereum_price': data['ethereum']['usd'],
    }

def load(ti):
    data = ti.xcom_pull(task_ids='transform')
    conn = psycopg2.connect(
        host="localhost",
        database="crypto_db",
        user="gitau",
        password="pass123"
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id SERIAL PRIMARY KEY,
            bitcoin_price FLOAT,
            ethereum_price FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("""
        INSERT INTO crypto_prices (bitcoin_price, ethereum_price)
        VALUES (%s, %s)
    """, (data['bitcoin_price'], data['ethereum_price']))
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id='crypto_price_etl',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='*/5 * * * *',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=lambda ti: transform(ti.xcom_pull(task_ids='extract'))
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load
    )

    extract_task >> transform_task >> load_task
