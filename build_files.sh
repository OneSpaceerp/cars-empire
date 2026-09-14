#!/bin/bash
echo '=== Installing Dependencies ==='
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo '=== Collecting Static Assets ==='
python3 cars_empire/cars_empire/cars_empire_backend/manage.py collectstatic --noinput --settings=cars_empire_project.settings_vercel

echo '=== Ready for Vercel Serverless Execution ==='
