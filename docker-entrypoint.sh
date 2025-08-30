#!/usr/bin/env bash
set -e

# Wait for DB to be available (simple loop)
if [ -n "${DATABASE_HOST:-}" ]; then
  echo "Waiting for database ${DATABASE_HOST}:${DATABASE_PORT:-5432}..."
  until python - <<PY
import sys, socket, os
host=os.environ.get("DATABASE_HOST")
port=int(os.environ.get("DATABASE_PORT","5432"))
try:
    s=socket.socket()
    s.settimeout(1)
    s.connect((host, port))
    s.close()
    print("db ok")
except Exception as e:
    sys.exit(1)
PY
  do
    sleep 1
  done
fi

# Collect static (optional - only if you use STATIC_ROOT)
if [ "$DJANGO_COLLECTSTATIC" = "1" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

# Apply database migrations
echo "Apply database migrations..."
python manage.py migrate --noinput

# Create superuser if env var set (non-interactive)
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser (if not exists)..."
  python - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
u="$DJANGO_SUPERUSER_EMAIL"
p="$DJANGO_SUPERUSER_PASSWORD"
if not User.objects.filter(email=u).exists():
    User.objects.create_superuser(username=u.split('@')[0], email=u, password=p)
    print("Superuser created")
else:
    print("Superuser already exists")
PY
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn auctioncraft_api.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --log-level ${GUNICORN_LOGLEVEL:-info}
