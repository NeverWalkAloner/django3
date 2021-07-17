#!/bin/sh

# Wait for postgres to start
/wait

echo "applying migrations"
python manage.py migrate --noinput

echo "running server"
python manage.py runserver 0.0.0.0:8080