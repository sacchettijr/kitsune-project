#!/bin/sh

# espera o RabbitMQ server iniciar
sleep 10

su -m myuser -c "celery -A projeto worker -l info"