#!/bin/sh
echo "Running migrations..."
python manage.py migrate
echo "Migrations completed"

python manage.py ensure_groups