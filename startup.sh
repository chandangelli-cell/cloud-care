#!/bin/bash
# Azure App Service Linux startup script for CloudCare HMS
echo "Starting CloudCare HMS on Azure App Service..."

# Run database schema initialization
python -m flask --app run.py init-db

# Launch Gunicorn WSGI server
gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 2 --timeout 600 run:app
