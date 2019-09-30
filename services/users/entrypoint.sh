#!/bin/sh
echo "Waiting for postgres..."

while ! nc -z users-db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"
gunicorn -b 0.0.0.0:5000 manage:app \
        --access-logfile "/var/log/ingme/access.log" \
        --error-logfile "/var/log/ingme/error.log" \
        --log-level DEBUG \
        --reload