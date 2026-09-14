import os
import sys
from pathlib import Path

# Resolve base directory
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'cars_empire' / 'cars_empire' / 'cars_empire_backend'

# Add backend directory to sys.path
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_empire_project.settings_vercel')

import django
django.setup()

# Auto-migrate for ephemeral SQLite in /tmp if no external DATABASE_URL is configured
if not os.environ.get('DATABASE_URL'):
    db_file = Path('/tmp/db.sqlite3')
    flag_file = Path('/tmp/.migrated')
    if not flag_file.exists():
        try:
            from django.core.management import call_command
            print('Initializing ephemeral test database in /tmp...')
            call_command('migrate', interactive=False)
            flag_file.touch()
            print('Database initialization complete.')
        except Exception as e:
            print(f'Database auto-init note: {e}')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Alias for Vercel Python runtime
app = application
handler = application
