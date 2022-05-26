from .staging import *

SECRET_KEY = os.environ.get('BACKEND_SECRET_KEY', 'django-secure-rz2zx%7x38d7vw6sy=&93qwyjax@-9#!cu8hjyxy8hj=7)4uz2')

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('BACKEND_DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('BACKEND_DB_NAME', 'backend_db'),
        'USER': os.environ.get('BACKEND_DB_USER', 'backend_user'),
        'PASSWORD': os.environ.get('BACKEND_DB_PASSWORD', 'backend_password'),
        'HOST': os.environ.get('BACKEND_DB_HOST', 'localhost'),
        'PORT': os.environ.get('BACKEND_DB_PORT', 5432)
    }
}


# Caching
# https://docs.djangoproject.com/en/4.0/topics/cache/#setting-up-the-cache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True

USE_X_FORWARDED_PORT = True

# EMAIL CONFIG
EMAIL_BACKEND = 'django_mailjet.backends.MailjetBackend'
MAILJET_API_KEY = decouple_config('API_KEY')
MAILJET_API_SECRET = decouple_config('API_SECRET')
EMAIL_HOST = 'in-v3.mailjet.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = decouple_config("EMAIL_HOST_API_KEY")
# EMAIL_HOST_PASSWORD = decouple_config("EMAIL_HOST_API_SECRET")
# EMAIL_USE_TLS = True




ALLOWED_HOSTS = ['avaloqsassets.com', 'www.avaloqsassets.com']

