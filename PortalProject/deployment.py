import os 
from .settings import * 
from .settings import BASE_DIR
import dj_database_url  # This library helps parse database URLs

ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', '')]  
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('WEBSITE_HOSTNAME', '')]
DEBUG = False


# Middleware setup with WhiteNoise for static file serving
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
# Set up database connection for Azure or local
if os.environ.get('USE_AZURE_DATABASE', False):  # Use this flag to toggle between environments
    # Azure PostgreSQL settings
    connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING', '')
    parameters = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split() if '=' in pair}

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parameters['dbname'],
            'USER': parameters['user'],
            'PASSWORD': parameters['password'],
            'HOST': parameters['host'],
            'PORT': parameters.get('port', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }
else:
    # Local database (e.g., SQLite or local PostgreSQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # Or 'django.db.backends.sqlite3' for SQLite
            'NAME': 'your_local_dbname',  # Change this to your local database name
            'USER': 'your_local_user',
            'PASSWORD': 'your_local_password',
            'HOST': 'localhost',
            'PORT': '5432',  # Default PostgreSQL port for local
        }
    }

# if connection_string:
#     DATABASES = {
#         'default': dj_database_url.parse(connection_string, conn_max_age=600, ssl_require=True)
#     }
# else:
#     # Optional: Fallback or error handling if connection string is missing
#     print("Warning: AZURE_POSTGRESQL_CONNECTIONSTRING environment variable not set.")
    # Raise an error, fallback to local DB, or handle as needed
