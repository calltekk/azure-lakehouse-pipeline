from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

# In real deployment, you'd use:
# - DatabricksSubmitRunOperator (Databricks)
# - AzureDataLakeStorage / Wasb / ADLS hooks
# - SparkSubmitOperator (if Spark cluster reachable)
# - PythonOperator for small steps
#
# Here we keep it "Airflow-shaped" but infra-agnostic.

with DAG(
    dag_id="pipeline01_end_to_end",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["pipeline01", "bronze-silver-gold"],
) as dag:
    start = EmptyOperator(task_id="start")

    bronze_streaming = EmptyOperator(task_id="bronze_streaming_job_placeholder")
    silver_streaming = EmptyOperator(task_id="silver_streaming_job_placeholder")
    gold_batch = EmptyOperator(task_id="gold_batch_job_placeholder")
    load_postgres = EmptyOperator(task_id="load_postgres_placeholder")

    end = EmptyOperator(task_id="end")

    start >> bronze_streaming >> silver_streaming >> gold_batch >> load_postgres >> end
