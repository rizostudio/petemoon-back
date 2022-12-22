from config.settings.common import *

# PRODUCTION APPS CONFIGURATION
INSTALLED_APPS = ("corsheaders",) + INSTALLED_APPS + ("gunicorn",)
# PRODUCTION APPS CONFIGURATION

# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env("DEFAULT_DATABASE_NAME"),
        "USER": get_env("DEFAULT_DATABASE_USER"),
        "PASSWORD": get_env("DEFAULT_DATABASE_PASSWORD"),
        "HOST": get_env("DEFAULT_DATABASE_HOST"),
        "PORT": get_env("DEFAULT_DATABASE_PORT"),
    }
}

# END DATABASE CONFIGURATION

# CORSHEADERS CONFIGURATION
CSRF_TRUSTED_ORIGINS = get_env("CSRF_TRUSTED_ORIGINS", default="").split(",")
CSRF_COOKIE_DOMAIN = get_env("CSRF_COOKIE_DOMAIN", optinal=True)
CORS_ORIGIN_REGEX_WHITELIST = [r".*"]  # TODO fill this
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True
MIDDLEWARE += ("corsheaders.middleware.CorsMiddleware",)
CORS_URLS_REGEX = r".*"  # TODO fill this
# END CORSHEADERS CONFIGURATION
DEBUG = get_env("DEBUG") == "True"

SECRET_KEY = get_env("SECRET_KEY")
