from __future__ import annotations

import os
import psycopg2


def main() -> None:
    # In real run, you'd read from Gold (Delta/Parquet) and upsert to Postgres.
    # This script is a placeholder that demonstrates secure config via env vars.

    host = os.environ.get("PGHOST", "")
    db = os.environ.get("PGDATABASE", "")
    user = os.environ.get("PGUSER", "")
    password = os.environ.get("PGPASSWORD", "")

    if not all([host, db, user, password]):
        raise SystemExit("Missing PGHOST/PGDATABASE/PGUSER/PGPASSWORD env vars.")

    conn = psycopg2.connect(host=host, dbname=db, user=user, password=password, sslmode="require")
    conn.autocommit = True

    with conn.cursor() as cur:
        with open("postgres/ddl/001_create_tables.sql", "r", encoding="utf-8") as f:
            cur.execute(f.read())

    conn.close()
    print("Postgres tables ensured (DDL applied).")


if __name__ == "__main__":
    main()
