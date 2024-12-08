from .core.core.settings import *
from .core.core.keep_safe import PROD_SECRET_KEY   , PROD_DATABASE_PASSWORD# Corrected the import statement

# Use the imported PROD_SECRET_KEY
SECRET_KEY = PROD_SECRET_KEY

ALLOWED_HOSTS = ['75.119.133.13']

# Use environment variables or hardcoded values for sensitive data



DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bitprod',
        'USER': 'bitproduser',
        'PASSWORD': PROD_DATABASE_PASSWORD,
        'HOST': '75.119.133.13',  # Or another host if the database is remote
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'core.urls'

# Static and Media settings
STATIC_URL = '/static/'
STATIC_ROOT = '/home/badolo/backend-B/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/badolo/backend-B/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/badolo/backend-B/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
