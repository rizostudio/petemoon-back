from config.settings.common import *

# DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# END DEBUG CONFIGURATION

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zmk1c2%=a2k@mj)e-ibe+4!-w9&(p9uan0*6i2vd$nkeh10uqf"
JWT_SECRET = SECRET_KEY
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
