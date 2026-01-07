# pipeline01 architecture

## Goal
A reference end-to-end data platform pattern using:
- Kafka/Event Hubs for ingestion
- Spark for processing (bronze/silver/gold)
- Postgres as a serving layer
- Airflow for orchestration

## Data flow
Producer (synthetic events) -> Kafka/Event Hubs -> Spark streaming -> Bronze (raw)
Bronze -> Spark streaming -> Silver (clean)
Silver -> Spark batch -> Gold marts
Gold -> Postgres tables

## Security
- No secrets in repo
- All creds via environment variables / Key Vault in real deployment
- Synthetic data only
