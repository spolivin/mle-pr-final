import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from steps.inference_data import create_table, extract, load
from steps.messages import send_telegram_success_message, send_telegram_failure_message


with DAG(
    dag_id='load_candidates_inference_etl',
    start_date=days_ago(7),
    schedule='10 21 * * 6',
    catchup=False,
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
    tags=["ETL", "Candidates", "Inference"],
) as dag:
    create_table_step = PythonOperator(task_id='create_table', python_callable=create_table)
    extract_step = PythonOperator(task_id='extract', python_callable=extract)
    load_step = PythonOperator(task_id='load', python_callable=load)

    create_table_step >> extract_step
    extract_step >> load_step