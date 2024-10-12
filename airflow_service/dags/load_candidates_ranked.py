from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from steps.ranked_data import (
    create_table,
    extract_candidates_train,
    extract_candidates_inference,
    train_model_infer,
    load,
)
from steps.messages import send_telegram_success_message, send_telegram_failure_message


with DAG(
    dag_id="rank_candidates_etl",
    start_date=days_ago(7),
    schedule="15 21 * * 6",
    catchup=False,
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
    tags=["ETL", "Candidates", "Ranking"],
) as dag:
    create_table_step = PythonOperator(
        task_id="create_table", python_callable=create_table
    )
    extract_train_step = PythonOperator(
        task_id="extract_candidates_train", python_callable=extract_candidates_train
    )
    extract_inference_step = PythonOperator(
        task_id="extract_candidates_inference",
        python_callable=extract_candidates_inference,
    )
    train_rank_step = PythonOperator(
        task_id="train_model_infer", python_callable=train_model_infer
    )
    load_step = PythonOperator(task_id="load", python_callable=load)

    create_table_step >> [extract_train_step, extract_inference_step]
    [extract_train_step, extract_inference_step] >> train_rank_step
    train_rank_step >> load_step
