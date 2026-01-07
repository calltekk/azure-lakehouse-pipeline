package com.example.pipeline01

import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

object GoldRevenueByDay {

  /**
    * Args:
    *   --silverPath <path>  (Delta table/path for Silver events)
    *   --goldPath <path>    (Delta output path for Gold mart)
    *
    * Example:
    *   --silverPath abfss://silver@youradls.dfs.core.windows.net/events/
    *   --goldPath   abfss://gold@youradls.dfs.core.windows.net/marts/fct_purchases_daily_scala
    */
  def main(args: Array[String]): Unit = {
    val params = parseArgs(args)

    val silverPath = required(params, "silverPath")
    val goldPath   = required(params, "goldPath")

    val spark = SparkSession.builder()
      .appName("pipeline01-gold-revenue-by-day")
      .getOrCreate()

    try {
      val silver = spark.read.format("delta").load(silverPath)

      // Expecting Silver columns (from your Python job):
      // event_ts (timestamp), event_type (string), price_gbp (double), user_id (string)
      val gold = buildGold(silver)

      gold.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(goldPath)

      println(s"Wrote Gold mart to: ")
    } finally {
      spark.stop()
    }
  }

  def buildGold(silver: DataFrame): DataFrame = {
    silver
      .where(col("event_type") === lit("purchase"))
      .where(col("event_ts").isNotNull)
      .withColumn("purchase_day", date_trunc("day", col("event_ts")))
      .groupBy(col("purchase_day"))
      .agg(
        count(lit(1)).as("purchases"),
        sum(col("price_gbp")).as("revenue_gbp"),
        countDistinct(col("user_id")).as("purchasing_users")
      )
      .orderBy(col("purchase_day"))
  }

  private def parseArgs(args: Array[String]): Map[String, String] = {
    // very small arg parser: --key value
    args.sliding(2, 2).collect {
      case Array(k, v) if k.startsWith("--") => k.drop(2) -> v
    }.toMap
  }

  private def required(params: Map[String, String], key: String): String = {
    params.getOrElse(key, throw new IllegalArgumentException(s"Missing --"))
  }
}
