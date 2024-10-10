
from .settings import *
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECRET_KEY = 'ul!v##s$6a#ud#0%142co4^g7=h!w^ghfyoj%!444i77ydz#ib'
# Use a simpler database for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
