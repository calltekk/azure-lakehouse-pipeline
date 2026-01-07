from __future__ import annotations

import json
import os
import random
import time
from datetime import datetime, timezone
from uuid import uuid4

import yaml
from confluent_kafka import Producer


EVENT_TYPES = ["page_view", "add_to_cart", "purchase"]
PRODUCT_IDS = [f"SKU-{i:04d}" for i in range(1, 301)]


def load_config() -> dict:
    cfg_path = os.environ.get("PIPELINE_CONFIG", "config/config.yml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_event() -> dict:
    event_type = random.choices(EVENT_TYPES, weights=[80, 15, 5], k=1)[0]
    product_id = random.choice(PRODUCT_IDS) if event_type != "page_view" else None
    price = round(random.uniform(4.99, 199.99), 2) if event_type == "purchase" else None

    return {
        "event_id": str(uuid4()),
        "event_ts": datetime.now(timezone.utc).isoformat(),
        "user_id": f"U-{random.randint(1, 500):04d}",
        "event_type": event_type,
        "session_id": str(uuid4()),
        "product_id": product_id,
        "price_gbp": price,
    }


def main() -> None:
    random.seed(42)
    cfg = load_config()

    kafka_cfg = cfg["kafka"]
    sasl_password = os.environ.get(kafka_cfg["sasl_password_env"], "")

    producer = Producer(
        {
            "bootstrap.servers": kafka_cfg["bootstrap_servers"],
            "security.protocol": kafka_cfg["security_protocol"],
            "sasl.mechanism": kafka_cfg["sasl_mechanism"],
            "sasl.username": kafka_cfg["sasl_username"],
            "sasl.password": sasl_password,
            # delivery settings
            "acks": "all",
            "retries": 5,
            "linger.ms": 50,
        }
    )

    topic = kafka_cfg["topic"]
    print(f"Producing synthetic events to topic: {topic}")

    while True:
        evt = build_event()
        producer.produce(topic, value=json.dumps(evt).encode("utf-8"))
        producer.poll(0)
        time.sleep(0.05)


if __name__ == "__main__":
    main()
