from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="weather_pipeline",
    default_args=DEFAULT_ARGS,
    description="Run Spark aggregation and write CSV to HDFS",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,  # lancement manuel
    catchup=False,
) as dag:

    run_spark_job = BashOperator(
        task_id="run_spark_job",
        bash_command=(
            "docker exec -i spark-master /spark/bin/spark-submit "
            "--master spark://spark-master:7077 "
            "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 "
            "/workspace/weather_spark.py"
        ),
    )

    run_spark_job
