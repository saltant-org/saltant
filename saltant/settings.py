"""
Django settings for saltant project.

There are two parts to this file. The first part deals with settings
that both Django and Celery workers need to worry about. The second part
deals with settings that only Django needs to worry about.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from datetime import timedelta
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# First part: Django and Celery worker settings

# Is this is a Celery worker?
IM_A_CELERY_WORKER = (
    False if os.environ['IM_A_CELERY_WORKER'] == 'False' else True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ['DEBUG'] == 'False' else True

# Celery settings
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_TIMEZONE = os.environ['CELERY_TIMEZONE']

# SSL settings
if os.environ['RABBITMQ_USES_SSL'] == 'True':
    import ssl

    BROKER_USE_SSL = {
        'cert_reqs': ssl.CERT_NONE,
    }

# Rollbar settings
PROJECT_USES_ROLLBAR = (
    False if os.environ['PROJECT_USES_ROLLBAR'] == 'False' else True)

if PROJECT_USES_ROLLBAR:
    ROLLBAR = {
        'access_token': os.environ['ROLLBAR_ACCESS_TOKEN'],
        'environment': 'development' if DEBUG else 'production',
        'root': BASE_DIR,
    }

# Second part: Django only settings

if not IM_A_CELERY_WORKER:
    # Make sure '.env' is secure
    SECRET_KEY = os.environ['SECRET_KEY']

    # Hosts - separate the comma-separated hosts and clean up any empty
    # strings caused by a terminal comma in ".env"
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].replace("'", "").split(',')
    ALLOWED_HOSTS = list(filter(None, ALLOWED_HOSTS))

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'splashpage.apps.SplashPageConfig',
        'tasksapi.apps.TasksApiConfig',
        'crispy_forms',
        'django_filters',
        'drf_yasg',
        'rest_framework',
        'rest_framework.authtoken',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
    ]

    ROOT_URLCONF = 'saltant.urls'

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
                    'splashpage.context_processors.export_env_vars',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'saltant.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DATABASE_NAME'],
            'USER': os.environ['DATABASE_USER'],
            'PASSWORD': os.environ['DATABASE_USER_PASSWORD'],
            'HOST': os.environ['DATABASE_HOST'],
            'PORT': os.environ['DATABASE_PORT'],
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
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
    # https://docs.djangoproject.com/en/2.0/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

    # REST framework settings
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'tasksapi.paginators.PageNumberVariableSizePagination',
        'PAGE_SIZE': 100,
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'EXCEPTION_HANDLER': (
            'rollbar.contrib.django_rest_framework.post_exception_handler'
        ),
    }

    # Swagger and ReDoc settings (see
    # https://drf-yasg.readthedocs.io/en/stable/settings.html)
    SWAGGER_SETTINGS = {
        'USE_SESSION_AUTH': False,
        'SECURITY_DEFINITIONS': {
            'Bearer': {
                'type': 'apiKey',
                'description': 'JWT access token (all users; transient)',
                'name': 'Authorization',
                'in': 'header',
            },
            'Token': {
                'type': 'apiKey',
                'description': 'DRF TokenAuthentication token (select users; permanent)',
                'name': 'Authorization',
                'in': 'header',
            },
        },
    }

    # JWT authentication settings (see
    # https://github.com/davesque/django-rest-framework-simplejwt)
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
        'REFRESH_TOKEN_LIFETIME': timedelta(weeks=35),
    }
