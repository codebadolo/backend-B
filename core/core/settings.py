"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from .keep_safe import PROD_SECRET_KEY   , PROD_DATABASE_PASSWORD# Corrected the import statement
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = PROD_SECRET_KEY
SECRET_KEY = 'ul!v##s$6a#ud#0%142co4^g7=h!w^ghfyoj%!444i77ydz#ib'
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
ALLOWED_HOSTS = [ '75.119.133.13' 'localhost' , '127.0.0.1']



DEBUG = True

# Application definition

INSTALLED_APPS = [
        
   # 'jazzmin',  # Add this at the top of your installed apps
       
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
       'rest_framework',  # Make sure this is included
    'django_countries',
    
    
    
    
     'drf_spectacular',
    'authentication',

     'transaction',
        'drf_yasg',
        
]

MIDDLEWARE = [

     
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
 #   'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
       #'csp.middleware.CSPMiddleware',  # Add this middleware directly
    'django_auto_logout.middleware.auto_logout',
   
]


'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bitprod',
        'USER': 'bitproduser',
        'PASSWORD': PROD_DATABASE_PASSWORD,
        'HOST': '75.119.133.13',  # Or another host if the database is remote
        'PORT': '5432',
    }
}
'''


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


'''CSP_DEFAULT_SRC = ["'self'"]
CSP_STYLE_SRC = ["'self'", 'maxcdn.bootstrapcdn.com']
CSP_SCRIPT_SRC = ["'self'", 'code.jquery.com']
'''

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000  # Enforce HTTPS for one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_COOKIE_SECURE = False




ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
#STATIC_ROOT  = 'static/'
STATIC_ROOT = '/home/badolo/backend-B/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    'http://75.119.133.13',
    'http://127.0.0.1',
      'http://localhost',
    # Add other trusted origins here
]

'''SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
   # 'LOGIN_URL': 'rest_framework:login',  # Configuring login URL for Swagger
  #  'LOGOUT_URL': 'rest_framework:logout',  # Configuring logout URL for Swagger
}'''

REDOC_SETTINGS = {
    'LAZY_RENDERING': True,
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
    # 
       "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        
    },
    # available SwaggerUI versions: https://github.com/swagger-api/swagger-ui/releases
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest", # default

}

'''JAZZMIN_SETTINGS = {
    "site_title": "BIT Admin",
    "site_header": "BIT Administration",
    "welcome_sign": "Welcome to BIT Admin",
    "site_logo": "path_to_logo/logo.png",
    "user_avatar": "path_to_profile_image",  # If you have a profile image for the user
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "transactions.Wallet": "fas fa-wallet",
        "transactions.Transaction": "fas fa-exchange-alt",
        "transactions.Currency": "fas fa-coins",
    },
    "custom_css": "custom.css",  # Add your custom CSS file if needed
    "custom_js": "custom.js",  # Add your custom JS file if needed
}
'''