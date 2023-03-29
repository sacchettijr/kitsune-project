#!/bin/sh

# espera o PostgreSQL iniciar
sleep 5

su -m myuser -c "python manage.py makemigrations"
su -m myuser -c "python manage.py migrate"
su -m root -c "gunicorn --bind 0.0.0.0:8000 projeto.wsgi"