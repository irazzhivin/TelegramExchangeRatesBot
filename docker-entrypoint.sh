#!/bin/bash

#echo "Collect static files"
#python manage.py collectstatic --noinput

#echo "Apply database migrations"
#python manage.py migrate

#echo "Load initial data"
#python manage.py loaddata initial_data

echo "Starting server"
./manage.py start
