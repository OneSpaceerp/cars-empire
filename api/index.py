import os
import sys
from pathlib import Path

# Resolve base directory
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'cars_empire' / 'cars_empire' / 'cars_empire_backend'

# Add directories to sys.path
FRONTEND_DIR = ROOT_DIR / 'cars_empire' / 'cars_empire' / 'cars_empire_frontend'
for p in (str(BACKEND_DIR), str(FRONTEND_DIR), str(ROOT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_empire_project.settings_vercel')

_django_app = None
_init_error = None

try:
    import django
    django.setup()
    from django.core.wsgi import get_wsgi_application
    _django_app = get_wsgi_application()
except Exception:
    import traceback
    _init_error = traceback.format_exc()
    print("DJANGO STARTUP ERROR:\n" + _init_error)

def app(environ, start_response):
    path_info = environ.get('PATH_INFO', '')
    
    # Setup/Migration endpoint
    if path_info in ('/setup-db', '/setup-db/', '/api/setup-db', '/api/setup-db/'):
        status = '200 OK'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        import io
        out = io.StringIO()
        try:
            from django.core.management import call_command
            call_command('migrate', interactive=False, stdout=out, stderr=out)
            result = "SUCCESS: Database migrated successfully!\n\n" + out.getvalue()
        except Exception:
            import traceback
            result = "ERROR: Migration failed:\n\n" + traceback.format_exc()
        return [result.encode('utf-8')]

    # If Django failed during cold start import, display the error
    if _init_error:
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        msg = "CARS EMPIRE STARTUP ERROR:\n\n" + _init_error
        return [msg.encode('utf-8')]
    
    # Execute normal Django request
    try:
        return _django_app(environ, start_response)
    except Exception:
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        import traceback
        tb = traceback.format_exc()
        print("REQUEST EXCEPTION:\n" + tb)
        msg = "CARS EMPIRE REQUEST ERROR:\n\n" + tb + "\n\nTip: You can initialize/migrate the database by visiting /setup-db/"
        return [msg.encode('utf-8')]

handler = app
application = app
