# Batch job: builds marts (gold) from Silver and writes Gold delta tables.

from pyspark.sql import functions as F

SILVER_PATH = "{{ silver_path }}"
GOLD_PATH = "{{ gold_path }}"

silver = spark.read.format("delta").load(SILVER_PATH)

dim_users = (
    silver.groupBy("user_id")
    .agg(
        F.min("event_ts").alias("first_seen_at"),
        F.max("event_ts").alias("last_seen_at"),
        F.count("*").alias("total_events"),
    )
)

dim_products = (
    silver.where(F.col("product_id").isNotNull())
    .groupBy("product_id")
    .agg(
        F.sum(F.when(F.col("event_type") == "add_to_cart", 1).otherwise(0)).alias("add_to_cart_events"),
        F.sum(F.when(F.col("event_type") == "purchase", 1).otherwise(0)).alias("purchase_events"),
    )
)

fct_purchases_daily = (
    silver.where(F.col("event_type") == "purchase")
    .groupBy(F.date_trunc("day", "event_ts").alias("purchase_day"))
    .agg(
        F.count("*").alias("purchases"),
        F.sum("price_gbp").alias("revenue_gbp"),
        F.countDistinct("user_id").alias("purchasing_users"),
    )
    .orderBy("purchase_day")
)

dim_users.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}/dim_users")
dim_products.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}/dim_products")
fct_purchases_daily.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}/fct_purchases_daily")
