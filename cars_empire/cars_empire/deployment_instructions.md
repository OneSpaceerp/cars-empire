# Deployment Instructions for Cars Empire on cPanel Shared Hosting

These instructions provide a general guide for deploying the Cars Empire Django application on a typical cPanel shared hosting environment that supports Python applications (often via Phusion Passenger or a similar setup).

**Disclaimer:** Specific steps might vary slightly depending on your hosting provider and their cPanel configuration. Always refer to your host's documentation if you encounter issues.

## 1. Prepare Project Files

Before uploading, ensure you have the project package (`cars_empire_deployment.zip`) provided to you. This package should contain:

*   `cars_empire_backend/`: The main Django project directory.
*   `cars_empire_frontend/`: Directory containing HTML templates (if separate).
*   `requirements.txt`: List of Python dependencies.
*   This `deployment_instructions.md` file.

## 2. Upload Project Files to cPanel

1.  Log in to your cPanel account.
2.  Navigate to the **File Manager**.
3.  Choose a location for your project. A common practice is to create a directory outside the `public_html` folder (e.g., `/home/your_cpanel_user/repositories/cars_empire`).
4.  Upload the `cars_empire_deployment.zip` file to this chosen directory.
5.  Select the uploaded zip file and click **Extract**.

## 3. Set Up Python Application in cPanel

1.  In cPanel, find the **Software** section and click on **Setup Python App** (or similar, e.g., "Python Selector").
2.  Click **Create Application**.
3.  Configure the application:
    *   **Python version:** Select a compatible version (e.g., 3.9, 3.10, or as available). The project was developed with Python 3.10.
    *   **Application root:** Enter the path to the directory where you extracted the `cars_empire_backend` folder (e.g., `/home/your_cpanel_user/repositories/cars_empire/cars_empire_backend`).
    *   **Application URL:** Choose the domain/subdomain where you want the site to be accessible (e.g., `carsempire.yourdomain.com` or `yourdomain.com/cars`).
    *   **Application startup file:** Leave this blank for now, or if required, enter `passenger_wsgi.py` (we will create this later).
    *   **Application Entry point:** Leave this blank for now, or if required, enter `application` (we will define this in `passenger_wsgi.py`).
4.  Click **Create**.

## 4. Install Dependencies

1.  After the application is created, the cPanel interface should show details, including a command to enter the virtual environment. Copy this command (it will look something like `source /home/your_cpanel_user/virtualenv/yourapplication/3.10/bin/activate`).
2.  Go back to the cPanel main page and open the **Terminal** (under the **Advanced** section).
3.  Paste the command copied in step 1 and press Enter to activate the virtual environment. You should see the environment name in your prompt (e.g., `(yourapplication:3.10)`).
4.  Navigate to your application root directory using the `cd` command:
    ```bash
    cd /home/your_cpanel_user/repositories/cars_empire/cars_empire_backend
    ```
5.  Install the required packages using pip and the `requirements.txt` file:
    ```bash
    pip install --upgrade pip
    pip install -r ../requirements.txt 
    ```
    *(Note: The `requirements.txt` file is assumed to be one level up from the `cars_empire_backend` directory based on the zip structure)*

## 5. Configure Database

Most shared hosting uses MySQL or MariaDB. You'll need to create a database and a user for your application.

1.  In cPanel, go to **Databases** -> **MySQL Databases** (or similar).
2.  **Create New Database:** Enter a name (e.g., `carsempire_db`) and click **Create Database**.
3.  **MySQL Users:** Create a new user. Enter a username (e.g., `carsempire_user`) and generate a strong password. Click **Create User**.
4.  **Add User To Database:** Select the user and database you just created, click **Add**. On the next screen, grant **All Privileges** to the user for that database.
5.  **Record Database Details:** Note down the database name, username, and password (including any prefixes cPanel might add, like `yourcpaneluser_`).

## 6. Update Django Settings (`settings.py`)

1.  Go back to the **File Manager** in cPanel.
2.  Navigate to `/home/your_cpanel_user/repositories/cars_empire/cars_empire_backend/cars_empire_project/`.
3.  Edit the `settings.py` file.
4.  **Update `SECRET_KEY`:** Replace the placeholder secret key with a new, strong, randomly generated key. You can use online Django secret key generators.
5.  **Update `DEBUG`:** Set `DEBUG = False` for production.
6.  **Update `ALLOWED_HOSTS`:** Add your domain name(s) to the list:
    ```python
    ALLOWED_HOSTS = ["carsempire.yourdomain.com", "www.carsempire.yourdomain.com"] # Replace with your actual domain(s)
    ```
7.  **Update `DATABASES`:** Modify the `default` database configuration to use the MySQL database details you created:
    ```python
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql", # Use mysql
            "NAME": "yourcpaneluser_carsempire_db", # Replace with your DB name
            "USER": "yourcpaneluser_carsempire_user", # Replace with your DB user
            "PASSWORD": "your_database_password", # Replace with your DB password
            "HOST": "localhost", # Usually localhost on shared hosting
            "PORT": "3306", # Default MySQL port
            "OPTIONS": {
                "init_command": "SET sql_mode=\"STRICT_TRANS_TABLES\"",
            },
        }
    }
    ```
    *   **Important:** You might need to install the MySQL client library in your virtual environment if it wasn't included or if `psycopg2-binary` causes issues: Activate the virtual environment in the terminal (Step 4.3) and run `pip install mysqlclient`.
8.  **Configure `STATIC_ROOT`:** Define where Django should collect static files. This should be a directory accessible by the web server, often within `public_html`.
    ```python
    STATIC_URL = "/static/"
    STATIC_ROOT = "/home/your_cpanel_user/public_html/static/cars_empire" # Example path
    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/home/your_cpanel_user/public_html/media/cars_empire" # Example path for user uploads
    ```
    *   Ensure the directories specified in `STATIC_ROOT` and `MEDIA_ROOT` exist or create them via File Manager.
9.  Save the changes to `settings.py`.

## 7. Create WSGI Entry Point (`passenger_wsgi.py`)

1.  In the **File Manager**, navigate to the application root directory (e.g., `/home/your_cpanel_user/repositories/cars_empire/cars_empire_backend`).
2.  Create a new file named `passenger_wsgi.py`.
3.  Edit the file and add the following content, adjusting paths if necessary:
    ```python
    import os
    import sys
    
    # Add the project root directory to the Python path
    sys.path.insert(0, os.path.dirname(__file__))
    
    # Add the virtual environment site-packages to the Python path
    # Adjust the path based on your cPanel setup and Python version
    # Example path:
    venv_path = "/home/your_cpanel_user/virtualenv/yourapplication/3.10/lib/python3.10/site-packages"
    sys.path.insert(0, venv_path)
    
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ["DJANGO_SETTINGS_MODULE"] = "cars_empire_project.settings"
    
    # Import the Django WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    ```
    *   **Crucial:** Replace `/home/your_cpanel_user/virtualenv/yourapplication/3.10/lib/python3.10/site-packages` with the actual path to your virtual environment's `site-packages` directory. You can find this path in the **Setup Python App** section in cPanel.
4.  Save the `passenger_wsgi.py` file.
5.  Go back to **Setup Python App** in cPanel, select your application, and ensure the **Application startup file** is set to `passenger_wsgi.py` and **Application Entry point** is set to `application`.

## 8. Run Initial Django Commands

1.  Open the **Terminal** in cPanel again.
2.  Activate the virtual environment (Step 4.3).
3.  Navigate to the Django project directory (`cars_empire_backend`):
    ```bash
    cd /home/your_cpanel_user/repositories/cars_empire/cars_empire_backend
    ```
4.  Apply database migrations:
    ```bash
    python manage.py migrate
    ```
5.  Collect static files:
    ```bash
    python manage.py collectstatic --noinput
    ```
    This will copy all static files (CSS, JS, images) from your apps into the `STATIC_ROOT` directory you defined in `settings.py`.
6.  Create a superuser if you haven't already (or if the SQLite one needs replacing for the new DB):
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email, and password.

## 9. Restart the Application

1.  Go back to the **Setup Python App** section in cPanel.
2.  Find your application.
3.  Click the **Restart** button (often looks like a circular arrow).

## 10. Access Your Website

Your Cars Empire website should now be accessible at the URL you configured in Step 3. You should also be able to access the Django admin panel by appending `/admin/` to your URL (e.g., `http://carsempire.yourdomain.com/admin/`) and logging in with the superuser credentials.

## Troubleshooting

*   **500 Internal Server Error:** Check the application logs. In **Setup Python App**, there's usually a link to the log file (`stderr.log`). This often contains detailed Python tracebacks.
*   **Static Files Not Loading (404):**
    *   Ensure `DEBUG = False` in `settings.py`.
    *   Verify `STATIC_ROOT` is correctly set and points to a publicly accessible directory.
    *   Confirm you ran `python manage.py collectstatic`.
    *   Check file permissions for the `STATIC_ROOT` directory.
    *   Your hosting provider might require additional configuration (e.g., in `.htaccess`) to serve static files correctly. Consult their documentation.
*   **Database Errors:** Double-check the database name, username, password, and host in `settings.py`. Ensure the user has all privileges on the database.
*   **Module Not Found Errors:** Ensure the virtual environment is activated correctly and all dependencies from `requirements.txt` were installed without errors. Check the paths in `passenger_wsgi.py`.
*   **Passenger Errors:** Consult your hosting provider's documentation regarding Phusion Passenger configuration and logs.

Good luck with the deployment!
