import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / 'cars_empire' / 'cars_empire' / 'cars_empire_backend'
FRONTEND_DIR = ROOT_DIR / 'cars_empire' / 'cars_empire' / 'cars_empire_frontend'

for p in (str(BACKEND_DIR), str(FRONTEND_DIR), str(ROOT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_empire_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

app = application
handler = application
