from .settings import *

DEBUG = True
PREPEND_WWW = None

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME", "carbon_usage_db"),
        "USER": os.getenv("DB_USER", "carbon_usage_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "qwertyuiop"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
