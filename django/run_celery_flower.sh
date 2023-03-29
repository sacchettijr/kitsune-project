#!/bin/sh

# espera o RabbitMQ server iniciar
sleep 15

su -m myuser -c "celery -A projeto flower -l info"