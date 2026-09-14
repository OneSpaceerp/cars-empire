import os
from pathlib import Path
import sys

# Install PyMySQL as MySQLdb if available (pure-python, safe on serverless)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Import all base settings
from .settings import *

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security & Debug for testing
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-vercel-testing-key-cars-empire-2026')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')

# Allowed Hosts for Vercel and custom domains
ALLOWED_HOSTS = [
    '*',
    '.vercel.app',
    'carsempire.net',
    'www.carsempire.net',
    'localhost',
    '127.0.0.1',
    'testserver',
]

# Database configuration: support DATABASE_URL (Neon / Supabase / Postgres / MySQL)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to SQLite (in /tmp for Vercel serverless writable storage)
    db_path = '/tmp/db.sqlite3' if os.environ.get('VERCEL') else str(BASE_DIR / 'db.sqlite3')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
        }
    }

# WhiteNoise for Static Assets
# Insert WhiteNoise right after SecurityMiddleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    sec_idx = 0
    for i, m in enumerate(MIDDLEWARE):
        if 'SecurityMiddleware' in m:
            sec_idx = i + 1
            break
    MIDDLEWARE.insert(sec_idx, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Static directories to collect
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR.parent / 'cars_empire_frontend' / 'static',
]
# Filter out non-existent static dirs to prevent warnings
STATICFILES_DIRS = [d for d in STATICFILES_DIRS if d.exists()]

# WhiteNoise storage: compressed manifest with fallback
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Templates directory resolution
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR.parent / 'cars_empire_frontend' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

# CORS & CSRF for testing
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://carsempire.net',
    'https://www.carsempire.net',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Relax cookie security for easy multi-domain testing if not production
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
