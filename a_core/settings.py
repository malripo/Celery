"""
Django settings for a_core project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import dj_database_url

# for environment
from environ import Env
env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')
# ENVIRONMENT='production'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-&w^we1bm(v_z-iv59a=2xf*+(rj3@g%guu$z=4qy(ei9j5&aci'
SECRET_KEY = env('SECRET_KEY')

# ENCRYPT_KEY = b'Xus2PqfZscJ6CWPFkt0s3-N9TsLsM3U5_x5vAztjxWc='
ENCRYPT_KEY = env('ENCRYPT_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# for environment
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

site_domain = env('RAILWAY_PUNLIC_DOMAIN', default='')

if ENVIRONMENT == "development":
    # ALLOWED_HOSTS = []
    # ALLOWED_HOSTS = ["*"]
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']
    CSRF_TRUSTED_ORIGINS = [ 'https://*' ]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'celery-production-155c.up.railway.app']
    CSRF_TRUSTED_ORIGINS = [ 'https://celery-production-155c.up.railway.app' ]

    # ALLOWED_HOSTS = ['localhost', '127.0.0.1', site_domain]
    # CSRF_TRUSTED_ORIGINS = [ 'https://{site_domain}']    

INTERNAL_IPS = (
    '127.0.0.1',
    'localhost:8000',
    'localhost:5555'
)

# Application definition
INSTALLED_APPS = [
    # for Channels
    "daphne",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # for allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    # Optional -- requires install using `django-allauth[socialaccount]`.
    'allauth.socialaccount',
    # for cleanup
    'django_cleanup.apps.CleanupConfig',
    # for django_htmx
    'django_htmx',
    # for app    
    'a_posts',
    'a_users',
    'a_home',
    'a_rtchat',
    'ajaxmethods',
    'a_messageboard',

    # for media server
    'cloudinary_storage',
    'cloudinary',
    # for honeypot
    "admin_honeypot",
    # for celery
    'django_celery_results', 
    'django_celery_beat',          
]

# for django-allauth
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # for allauth:
    'allauth.account.middleware.AccountMiddleware',
    # for django_htmx
    'django_htmx.middleware.HtmxMiddleware', 
    # for collectstatic
    "whitenoise.middleware.WhiteNoiseMiddleware",   
]

ROOT_URLCONF = 'a_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # fro allouth 이미 정의 됌
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# for Channels
WSGI_APPLICATION = 'a_core.wsgi.application'
ASGI_APPLICATION = 'a_core.asgi.application'

# for CHANNEL_LAYERS
if ENVIRONMENT == "development":
    # for local
    CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},        
    }  
else:
    # # for local or web
    # CHANNEL_LAYERS = {
    #     "default": {
    #         "BACKEND": "channels_redis.core.RedisChannelLayer",
    #         "CONFIG": {
    #             "hosts": [("localhost", 6379)],
    #         },
    #     },
    # }

    # for web railway(malripo) or render(eatplay)
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                # "hosts": [('redis://default:QFDwYIFVridTMLTbIiVvqEXHbsQVvOWi@yamabiko.proxy.rlwy.net:10275')],  # <=railway(malripo) [real_chat_redis]
                "hosts": [(env('REDIS_URL'))],
            },
        },
    }

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(env('DATABASE_URL'))
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# for static
STATIC_URL = '/static/'
STATICFILES_DIRS=[BASE_DIR / 'static']

# for whitenoise for collectstatic
STATIC_ROOT=BASE_DIR / 'staticfiles'

# for media server
MEDIA_URL = 'media/'
if ENVIRONMENT == "development":
    MEDIA_ROOT = BASE_DIR / 'media' 
else:    
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
            },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
    }
    CLOUDINARY_STORAGE = {
        # 'CLOUD_NAME': env('CLOUD_NAME'),
        # 'API_KEY': env('API_KEY'),
        # 'API_SECRET': env('API_SECRET'),
        'CLOUDINARY_URL':env('CLOUDINARY_URL')    
    }  

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# for login
LOGIN_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_REDIRECT_URL = "{% url 'account_signup' %}?next={% url 'profile-onboarding' %}"


# for email authentication
if ENVIRONMENT == "production" or ENVIRONMENT == "development":    
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env('EMAIL_ADDRESS')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    # DEFAULT_FROM_EMAIL = 'TTugTTag'
    DEFAULT_FROM_EMAIL = f'My Message Board {env("EMAIL_ADDRESS")}'      # <===Awesome은 Django App Name(My Message Board)
    ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_USERNAME_BLACKLIST = [ 'admin', 'accounts', 'profile', 'category', 'post' ]
ACCOUNT_USERNAME_BLACKLIST = [ 'admin', 'accounts', 'profile', 'category', 'post', 'inbox', 'theboss' ]

# CELERY SETTINGS
if ENVIRONMENT == "development":
    CELERY_BROKER_URL = 'redis://localhost:6379/0' 
else:
    CELERY_BROKER_URL = env('REDIS_URL')

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True