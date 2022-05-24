from .base import *

ALLOWED_HOSTS = ['*']

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

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "ava_caches_cache",
    }
}

STATIC_ROOT = BASE_DIR / "static"
