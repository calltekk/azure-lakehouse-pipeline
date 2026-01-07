# Azure Lakehouse Pipeline

A **production-shaped data engineering reference project** demonstrating how an event-driven analytics platform is typically built on Azure using **Kafka/Event Hubs, Spark, Airflow, and Postgres**.

This repository is intentionally designed to:
- mirror **real-world enterprise architectures**
- be **safe to share publicly** (synthetic data only)
- work with **restricted developer laptops** (no Docker required)
- act as a **template / learning reference**, not a toy demo

---

## Architecture Overview

**High-level flow:**

1. **Event ingestion**
   - Synthetic events are produced to Kafka (Azure Event Hubs Kafka-compatible endpoint)
2. **Streaming ingestion (Bronze)**
   - Spark Structured Streaming writes raw events to cloud storage
3. **Streaming cleansing (Silver)**
   - Events are parsed, typed, validated, and deduplicated
4. **Batch aggregation (Gold)**
   - Analytics-ready dimension and fact tables are produced
5. **Serving layer**
   - Curated Gold tables are loaded into Postgres
6. **Orchestration**
   - Airflow coordinates batch workloads and dependencies

**Data model pattern:** Bronze → Silver → Gold (Lakehouse)

---

## Tech Stack

| Layer | Technology |
|-----|-----------|
Ingestion | Kafka / Azure Event Hubs (Kafka API)
Processing | Apache Spark (Databricks or Synapse Spark)
Storage | Azure Data Lake Storage Gen2 (conceptual)
Serving | PostgreSQL
Orchestration | Apache Airflow
Config & Secrets | Environment variables / Key Vault (conceptual)

> Spark and Airflow are represented as **deployable code**, not local services.  
> This reflects how these systems are typically used in Azure environments.

---

## Repository Structure

```text
.
├── dags/                  # Airflow DAG definitions
├── spark/                 # Spark jobs (bronze / silver / gold)
├── spark-scala/           # Scala Spark jobs
├── kafka/                 # Kafka/Event Hubs producer + schemas
├── postgres/              # Serving-layer DDL and loaders
├── config/                # Example configuration (no secrets)
├── docs/                  # Architecture & runbook
├── tests/                 # Contract and unit tests
└── scripts/               # Local helper utilities
```


## What This Project Is (and Is Not)

### ✅ What this *is*
- A **realistic reference implementation**
- A clean example of **event-driven + batch analytics**
- Suitable for:
  - portfolio use
  - interview walkthroughs
  - internal knowledge sharing
  - extending into a real deployment

### ❌ What this is *not*
- A fully runnable local stack
- A Docker-based demo
- A production deployment

This separation is intentional and mirrors how modern data platforms are actually developed.

---

## Data Safety & Security

- **All data is synthetic**
- **No credentials are committed**
- Secrets are expected via:
  - environment variables
  - CI/CD secrets
  - Azure Key Vault (in real deployments)

The repository is safe to publish publicly.

---

## Local Development

What you *can* run locally:
- Unit tests:
  ```bash
  pytest


## Scala Spark Job

`spark-scala/` contains a minimal Scala Spark job used to build a Gold mart from Silver events.

- Input: Silver Delta path (typed/cleaned events)
- Output: Gold Delta mart `fct_purchases_daily_scala`

This module is intended to run on a Spark cluster (Databricks/Synapse/etc.). Spark is marked as `provided` in `build.sbt`.
