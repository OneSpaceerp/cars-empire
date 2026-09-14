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
application = get_wsgi_application()

# Alias for Vercel WSGI runner
app = application
handler = application
