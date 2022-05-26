from .base import *
DEPLOYMENT_ENVIRONMENT = decouple_config('DEPLOYMENT_ENVIRONMENT', default='local')

ALLOWED_HOSTS = ['*']

DEBUG = DEPLOYMENT_ENVIRONMENT not in ['production', 'staging']

INSTALLED_APPS += [
    'django.contrib.postgres',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'backend_db',
        'USER': 'backend_user',
        'PASSWORD': 'backend_password',
        'HOST': 'postgres',
        'PORT': 5432
    }
}


STATIC_ROOT = BASE_DIR / "static"
