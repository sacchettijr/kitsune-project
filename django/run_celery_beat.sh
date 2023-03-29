#!/bin/sh

# espera o RabbitMQ server iniciar
sleep 15

su -m myuser -c "rm /tmp/celerybeat-doshi.pid > /dev/null"
su -m myuser -c "celery -A projeto beat -l info --pidfile=/tmp/*.pid"