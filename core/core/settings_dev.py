
from .settings import *
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use a simpler database for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
