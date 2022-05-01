#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Install requirements
pip install -r requirements.txt
pip install -r requirements/local.txt

# Run database migrations
python manage.py migrate --noinput

# Start api server
python manage.py runserver 0.0.0.0:8000
