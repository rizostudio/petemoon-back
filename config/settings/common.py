from os import environ
from pathlib import Path

# GET ENV UTIL


def get_env(key, default=None, optinal=False):
    """Return environment variables with some options."""
    val = environ.get(key)
    if val is not None:
        return val
    elif default is not None:
        return default
    elif not optinal:
        raise ValueError(f"Environment variable {key} was not defined")


# END GET ENV UTIL


"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env(
    "SECRET_KEY",
    default=(
        "django-insecure-zmk1c2%=a2k@mj)e-ibe+4!-w9&(p9uan0*6i2vd$nkeh10uqf"
    ),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# APP CONFIGURATION
DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Admin panel and documentation:
    "django.contrib.admin",
    "django.contrib.admindocs",
)

THIRD_PARTY_APPS = ("rest_framework",)

# Apps specific for this project go here.
LOCAL_APPS = ("accounts",)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# END APP CONFIGURATION

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# END DATABASE CONFIGURATION


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = get_env("STATIC_ROOT", default="static/")
STATIC_URL = get_env("STATIC_URL", default="static/")
static_file_env = get_env("STATICFILES_DIRS", optinal=True)
STATICFILES_DIRS = (
    static_file_env.split(",") if static_file_env is not None else []
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", default="*").split(",")

# CACHING CONFIGURATION
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": get_env("REDIS_URL"),
    }
}
# END CACHING CONFIGURATION

# AUTH USER MODEL CONFIGURATION
AUTH_USER_MODEL = "accounts.User"
# END AUTH USER MODEL CONFIGURATION

# OTP CONFIGURATION
OTP_CODE_LENGTH = int(get_env("OTP_CODE_LENGTH", default="6"))
OTP_TTL = int(get_env("OTP_TTL", default="120"))
# END OTP CONFIGURATION

# JWT SETIINGS
ACCESS_TTL = int(get_env("ACCESS_TTL", default="300"))
REFRESH_TTL = int(get_env("REFRESH_TTL", default="86400"))
JWT_SECRET = get_env("JWT_SECRET", default=SECRET_KEY)
# END JWT SETTINGS

# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.authentication.JWTAuthentication",
    ),
}
# END REST FRAMEWORK CONFIGURATION
