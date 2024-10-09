from decouple import config

SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['75.119.133.13']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': ' 75.119.133.13',
        'PORT': '5432',
    }
}

# Other shared settings...
