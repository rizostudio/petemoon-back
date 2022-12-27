from config.settings.common import *

TEST_DISCOVER_PATTERN = "tests*.py"

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
