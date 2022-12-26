from config.settings.common import *

# DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# END DEBUG CONFIGURATION

# EMAIL CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# END EMAIL CONFIGURATION


# TOOLBAR CONFIGURATION
INSTALLED_APPS += ("django_extensions",)
# END TOOLBAR CONFIGURATION

# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# END DATABASE CONFIGURATION
