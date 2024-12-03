#!/bin/bash
python manage.py makemigrations
python manage.py makemigrations count
python manage.py makemigrations chat
python manage.py migrate 
python manage.py runserver 0.0.0.0:8000