#!/bin/bash

# Cars Empire Deployment Script
echo "Starting Cars Empire deployment..."

# Set the project directory
PROJECT_DIR="/home/carsempire/repositories/cars_empire"
BACKEND_DIR="$PROJECT_DIR/cars_empire_backend"
FRONTEND_DIR="$PROJECT_DIR/cars_empire_frontend"

# Navigate to backend directory
cd $BACKEND_DIR

# Activate virtual environment
source /home/carsempire/virtualenv/repositories/cars_empire/cars_empire_backend/3.10/bin/activate

# Install/update requirements
echo "Installing Python requirements..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --settings=cars_empire_project.settings_production

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=cars_empire_project.settings_production

# Create superuser if it doesn't exist
echo "Creating superuser (if needed)..."
python manage.py shell --settings=cars_empire_project.settings_production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@carsempire.net', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
EOF

# Set proper permissions
echo "Setting file permissions..."
chmod 755 $BACKEND_DIR
chmod 644 $BACKEND_DIR/passenger_wsgi.py
chmod 644 $BACKEND_DIR/.htaccess

# Restart the application
echo "Restarting application..."
touch $BACKEND_DIR/tmp/restart.txt

echo "Deployment completed successfully!"
echo "Your site should now be accessible at https://carsempire.net"
