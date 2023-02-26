from config.settings.common import *

TEST_DISCOVER_PATTERN = "tests*.py"
SECRET_KEY = (
    "django-insecure-zmk1c2%=a2k@mj)e-ibe+4!-w9&(p9uan0*6i2vd$nkeh10uqf"
)
JWT_SECRET = SECRET_KEY

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

DEBUG = True
