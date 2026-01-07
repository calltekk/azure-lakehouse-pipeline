# Reads from Kafka/Event Hubs and writes raw events to Bronze storage.
# Intended for Spark Structured Streaming (Databricks/Synapse Spark).

from pyspark.sql import functions as F
from pyspark.sql.types import StringType

KAFKA_BOOTSTRAP = "{{ kafka_bootstrap_servers }}"
KAFKA_TOPIC = "{{ kafka_topic }}"
BRONZE_PATH = "{{ bronze_path }}"


df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)

parsed = df.select(F.col("value").cast(StringType()).alias("raw_json"), F.current_timestamp().alias("ingested_at"))

(
    parsed.writeStream.format("delta")
    .option("checkpointLocation", f"{BRONZE_PATH}/_checkpoints/")
    .outputMode("append")
    .start(BRONZE_PATH)
)
