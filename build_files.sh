#!/bin/bash

# Exit on error
set -e

echo "Installing dependencies..."
/opt/vercel/python3/bin/python3 -m pip install -r requirements.txt

echo "Collecting static files..."
/opt/vercel/python3/bin/python3 manage.py collectstatic --noinput --clear
