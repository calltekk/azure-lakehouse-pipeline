# Reads Bronze delta, parses JSON, types columns, writes to Silver.

from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

BRONZE_PATH = "{{ bronze_path }}"
SILVER_PATH = "{{ silver_path }}"

schema = StructType(
    [
        StructField("event_id", StringType(), False),
        StructField("event_ts", StringType(), False),
        StructField("user_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("session_id", StringType(), False),
        StructField("product_id", StringType(), True),
        StructField("price_gbp", DoubleType(), True),
    ]
)

bronze = spark.readStream.format("delta").load(BRONZE_PATH)

silver = (
    bronze.select(F.from_json("raw_json", schema).alias("j"), "ingested_at")
    .select("j.*", "ingested_at")
    .withColumn("event_ts", F.to_timestamp("event_ts"))
    .filter(F.col("event_ts").isNotNull())
)

(
    silver.writeStream.format("delta")
    .option("checkpointLocation", f"{SILVER_PATH}/_checkpoints/")
    .outputMode("append")
    .start(SILVER_PATH)
)
