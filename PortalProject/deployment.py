import os 
from .settings import * 
from .settings import BASE_DIR
import dj_database_url  # This library helps parse database URLs


ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]  
CSRF_TRUSTED_ORGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME'] ]
DEBUG = False


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

# Database Already Changed to POSTGRE-SQL

connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING', '')
# parameters = {pair.split('='):pair.split('=')[1] for pair in connection_string.split(' ') }  If using sql-lite

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': parameters['dbname'],             
#         'USER': parameters['user'],            
#         'PASSWORD': parameters['password'],      
#         'HOST': parameters['host']              
#     }
# }

DATABASES = {
    'default': dj_database_url.parse(connection_string, conn_max_age=600, ssl_require=True)
}

