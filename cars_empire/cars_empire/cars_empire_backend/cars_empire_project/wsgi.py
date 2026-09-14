"""
WSGI config for cars_empire_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Resolve directory paths for serverless and traditional WSGI
BACKEND_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BACKEND_DIR.parent / 'cars_empire_frontend'
ROOT_DIR = BACKEND_DIR.parent.parent.parent

for p in (str(BACKEND_DIR), str(FRONTEND_DIR), str(ROOT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

settings_module = 'cars_empire_project.settings_vercel' if os.environ.get('VERCEL') else 'cars_empire_project.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

from django.core.wsgi import get_wsgi_application
_django_app = get_wsgi_application()

import threading
_db_ready = False
_db_lock = threading.Lock()

def ensure_database_ready():
    global _db_ready
    if _db_ready:
        return
    with _db_lock:
        if _db_ready:
            return
        try:
            from django.db import connection
            tables = connection.introspection.table_names()
            if 'django_migrations' not in tables or 'merchants_category' not in tables:
                from django.core.management import call_command
                call_command('migrate', interactive=False)
                try:
                    from cars_empire_project.seed_data import seed_demo_data
                    seed_demo_data()
                except Exception as seed_err:
                    print(f"Seed note: {seed_err}")
            _db_ready = True
        except Exception as e:
            print("Auto-migrate warning:", e)

def application(environ, start_response):
    ensure_database_ready()
    return _django_app(environ, start_response)

# Alias for Vercel WSGI runner
app = application
handler = application
