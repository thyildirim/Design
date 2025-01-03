#!/bin/bash

set -eu

python manage.py makemigrations
python manage.py migrate
