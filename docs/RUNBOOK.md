# Runbook (dev)

## Local
- You can run `kafka/producer_synth.py` only if you have a Kafka endpoint (e.g., Event Hubs Kafka).
- Spark jobs are intended for Databricks/Synapse Spark.
- Airflow DAG is a template; run in managed Airflow later.

## Azure (typical)
1. Create Event Hubs namespace + topic
2. Create ADLS Gen2 containers: bronze/silver/gold
3. Provision Databricks workspace + cluster
4. Deploy jobs:
   - bronze_ingest (streaming)
   - silver_cleanse (streaming)
   - gold_aggregate (batch)
5. Deploy Airflow and replace placeholders with real operators
6. Load Postgres from Gold outputs
