"""
Django settings for smmproject project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from decouple import config
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tr(p6ex$ewh*+0s6p)i@18m9q3y00qk(=le(og&^j_a%1e)^jq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    'customer_analytics',
    'marketing_campaigns',
    'social_management',
    'rest_framework',
    'surveys',
    'corsheaders',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Agregar este middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smmproject.urls'

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

WSGI_APPLICATION = 'smmproject.wsgi.application'
#CORS_ALLOWED_ORIGINS = [
#    "https://villaizan-social.onrender.com/",
#    "http://127.0.0.1:8000/",
#]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'Accept-Encoding',
    'Authorization',
    'Content-Type',
    'dnt',
    'Content-Length',
    'origin',
    'user-agent',
    'X-CSRF-Token',
    'x-requested-with',
    'Access-Control-Allow-Origin'
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'HolaMundo2025',
        'HOST': 'dp2-pruebas-2c.cybvloot89zv.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}



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

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Configuración para la autenticación de Facebook e Instagram
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id', 'email', 'name', 'first_name', 'last_name',
            'verified', 'locale', 'timezone', 'link'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v12.0',
    },
    'instagram': {
        'METHOD': 'oauth2',
        'SCOPE': ['user_profile', 'user_media'],
        'FIELDS': ['id', 'username', 'account_type', 'media_count'],
        'EXCHANGE_TOKEN': True,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TIKTOK_CLIENT_ID = config('TIKTOK_CLIENT_ID')
TIKTOK_CLIENT_SECRET = config('TIKTOK_CLIENT_SECRET')

env = environ.Env()
environ.Env.read_env()  # Lee el archivo .env

# Configuración de AWS S3
#AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
#AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
#AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
#AWS_S3_SIGNATURE_NAME = env('AWS_S3_SIGNATURE_NAME')
#AWS_S3_FILE_OVERWRITE = False
#AWS_DEFAULT_ACL = None
#AWS_S3_VERIFY = True
#AWS_QUERYSTRING_AUTH = False
# Configuración de almacenamiento de medios
#MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}