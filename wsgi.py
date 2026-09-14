import os
import sys
from pathlib import Path
import traceback

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / 'cars_empire' / 'cars_empire' / 'cars_empire_backend'
FRONTEND_DIR = ROOT_DIR / 'cars_empire' / 'cars_empire' / 'cars_empire_frontend'

for p in (str(BACKEND_DIR), str(FRONTEND_DIR), str(ROOT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

settings_module = 'cars_empire_project.settings_vercel' if os.environ.get('VERCEL') else 'cars_empire_project.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

_django_app = None
_startup_error = None

try:
    from django.core.wsgi import get_wsgi_application
    _django_app = get_wsgi_application()
except Exception:
    _startup_error = traceback.format_exc()
    print("DJANGO STARTUP EXCEPTION:\n" + _startup_error)

def application(environ, start_response):
    global _django_app, _startup_error
    
    path_info = environ.get('PATH_INFO', '')
    
    # Setup / Migrate endpoint on demand
    if path_info.rstrip('/') in ('/setup-db', '/api/setup-db'):
        start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
        import io
        out = io.StringIO()
        try:
            from django.core.management import call_command
            call_command('migrate', interactive=False, stdout=out, stderr=out)
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                admin_email = 'admin@carsempire.net'
                admin_user = User.objects.filter(email=admin_email).first()
                if not admin_user:
                    admin_user = User.objects.create_superuser(
                        email=admin_email,
                        password='Admin123456!',
                        phone='+201000000000',
                        username='admin'
                    )
                    out.write(f"\nDefault admin created successfully!\nEmail: {admin_email}\nPassword: Admin123456!\n")
                else:
                    admin_user.set_password('Admin123456!')
                    admin_user.is_staff = True
                    admin_user.is_superuser = True
                    admin_user.save()
                    out.write(f"\nDefault admin credentials set!\nEmail: {admin_email}\nPassword: Admin123456!\n")
            except Exception as user_err:
                out.write(f"\nUser creation note: {user_err}\n")
            return [f"SUCCESS: Database migrated successfully!\n\n{out.getvalue()}".encode('utf-8')]
        except Exception:
            return [f"ERROR: Migration failed:\n\n{traceback.format_exc()}".encode('utf-8')]

    if _startup_error:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain; charset=utf-8')])
        return [f"CARS EMPIRE STARTUP ERROR:\n\n{_startup_error}".encode('utf-8')]
        
    try:
        return _django_app(environ, start_response)
    except Exception:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain; charset=utf-8')])
        err = traceback.format_exc()
        return [f"CARS EMPIRE REQUEST ERROR:\n\n{err}\n\nTip: Try visiting /setup-db to run migrations.".encode('utf-8')]

app = application
handler = application

