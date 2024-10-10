from decouple import config
from .base  import * 

ALLOWED_HOSTS = [ '75.119.133.13']
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
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
