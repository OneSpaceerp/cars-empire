import os
import sys

# Activate the virtual environment if needed
INTERP = os.path.expanduser("/home/carsempire/virtualenv/repositories/cars_empire/cars_empire_backend/3.10/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add the project directory to the Python path
sys.path.append(os.getcwd())

# Set the Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_empire_project.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
