# Azure Lakehouse Pipeline

A reference, production-shaped data engineering pipeline template:
- Kafka/Event Hubs ingestion
- Spark (bronze/silver/gold)
- Postgres serving layer
- Airflow orchestration

**Synthetic data only. No secrets committed.**

## What runs locally?
- Unit tests (`pytest`)
- Optional: synthetic producer if you have a Kafka endpoint (Event Hubs Kafka)

## Next steps
- Replace Airflow placeholders with your org's operators (DatabricksSubmitRunOperator, etc.)
- Parameterize Spark jobs using job params or widgets
- Add data quality tests (Great Expectations / Deequ)
