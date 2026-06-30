#!/usr/bin/env bash
set -e

echo "Ожидание готовности PostgreSQL ($POSTGRES_HOST:$POSTGRES_PORT)..."
python - <<'PY'
import os, time, socket
host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", "5432"))
for _ in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit("PostgreSQL недоступен")
print("PostgreSQL готов.")
PY

echo "Применение миграций Alembic..."
alembic upgrade head

exec "$@"
