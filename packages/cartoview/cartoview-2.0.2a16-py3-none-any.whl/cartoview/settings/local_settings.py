import os
import sys

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cartoview2',
        'USER': 'hishamkaram',
        'PASSWORD': 'clogic',
        'HOST': 'localhost',
        'PORT': '5432',
        # 'CONN_MAX_AGE': 30,
    },
}
OAUTH_SERVER_BASEURL = "http://indiana.multihazardmitigation.com"
WAGTAIL_SITE_NAME = "Cartoview"
SECRET_KEY = "c8(50gzg=^s6&m73&801%+@$24+&8duk$^^4ormfkbj!*q86fo"
ALLOWED_HOSTS = ['*']
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
ASYNC_ENABLED = strtobool(os.getenv('ASYNC_ENABLED', 'False'))
RABBITMQ_SIGNALS_BROKER_URL = os.getenv(
    'RABBITMQ_SIGNALS_BROKER_URL', 'amqp://localhost:5672')
REDIS_SIGNALS_BROKER_URL = os.getenv(
    'REDIS_SIGNALS_BROKER_URL', 'redis://localhost:6379/0')
LOCAL_SIGNALS_BROKER_URL = 'memory://'
CELERY_BROKER_URL = os.getenv(
    'CELERY_BROKER_URL', REDIS_SIGNALS_BROKER_URL if ASYNC_ENABLED else LOCAL_SIGNALS_BROKER_URL)
if ASYNC_ENABLED:
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_RESULT_PERSISTENT = False

# Allow to recover from any unknown crash.
CELERY_ACKS_LATE = True

# Set this to False in order to run async
CELERY_TASK_ALWAYS_EAGER = False if ASYNC_ENABLED else True
CELERY_TASK_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_RESULT_EXPIRES = 43200
CELERY_MESSAGE_COMPRESSION = 'gzip'
CELERY_MAX_CACHED_RESULTS = 32768
APPS_DIR = os.path.join(BASE_DIR, os.pardir, "cartoview_apps")
STAND_ALONE = True
if STAND_ALONE:

    # NOTE: load cartoview apps
    if APPS_DIR not in sys.path:
        sys.path.append(APPS_DIR)
    from cartoview.app_manager.config import CartoviewApp  # noqa
    CartoviewApp.load(apps_dir=APPS_DIR)
    for app in CartoviewApp.objects.get_active_apps().values():
        try:
            # ensure that the folder is python module
            app_module = __import__(app.name)
            app_dir = os.path.dirname(app_module.__file__)
            app_settings_file = os.path.join(app_dir, "settings.py")
            libs_dir = os.path.join(app_dir, "libs")
            if os.path.exists(app_settings_file):
                app_settings_file = os.path.realpath(app_settings_file)
                exec(open(app_settings_file).read())
            if os.path.exists(libs_dir) and libs_dir not in sys.path:
                sys.path.append(libs_dir)
            if app.name not in INSTALLED_APPS:
                INSTALLED_APPS += (app.name.__str__(), )
        except Exception as e:
            logger.error(str(e))
