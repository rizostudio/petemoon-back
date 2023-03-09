from config.settings.common import *

# PRODUCTION APPS CONFIGURATION
INSTALLED_APPS += ("corsheaders", "gunicorn")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env("SECRET_KEY")
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS").split(",")

# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env("DEFAULT_DATABASE_NAME"),
        "USER": get_env("DEFAULT_DATABASE_USER"),
        "PASSWORD": get_env("DEFAULT_DATABASE_PASSWORD"),
        "HOST": get_env("DEFAULT_DATABASE_HOST"),
        "PORT": get_env("DEFAULT_DATABASE_PORT"),
    }
}

# END DATABASE CONFIGURATION

# CORSHEADERS CONFIGURATION
ALLOWED_HOSTS=get_env("ALLOWED_HOSTS").split(",")
CORS_ALLOWED_ORIGINS = get_env("CORS_ALLOWED_ORIGINS").split(",")
CSRF_TRUSTED_ORIGINS = get_env("CSRF_TRUSTED_ORIGINS").split(",")
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True
MIDDLEWARE += ("corsheaders.middleware.CorsMiddleware",)
# END CORSHEADERS CONFIGURATION
DEBUG = get_env("DEBUG") == "True"

JWT_SECRET = get_env("JWT_SECRET", default=SECRET_KEY)

