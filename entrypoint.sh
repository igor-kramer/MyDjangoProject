#!/bin/bash

python manage.py migrate
python gunicorn mysite.wsgi:application --bind 0.0.0.0:8000