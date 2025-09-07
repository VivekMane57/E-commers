"""
Django settings for E_commers project.
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Base paths & .env
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ------------------------------------------------------------------
# Core settings
# ------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-unsafe-secret")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = ["*"]  # tighten in prod

# ------------------------------------------------------------------
# Installed apps
# ------------------------------------------------------------------
INSTALLED_APPS = [
    # WebSocket server - MUST be at the TOP
    'daphne',
    
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # 3rd-party
    "crispy_forms",
    "crispy_bootstrap5",
    "channels",  # Real-time WebSocket support

    # Local apps
    "E_commers",
    "accounts",
    "category",
    "store",
    "carts",
    "orders",
    "realtime",  # Real-time shopping app
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ← Make sure this line exists
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "E_commers.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "E_commers/templates",
            BASE_DIR / "accounts/templates",
            BASE_DIR / "store/templates",
            BASE_DIR / "realtime/templates",  # Add realtime templates
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Custom
                "category.context_processors.menu_links",
                "carts.context_processors.counter",
                "accounts.context_processors.user_profile",
            ],
        },
    },
]

WSGI_APPLICATION = "E_commers.wsgi.application"
ASGI_APPLICATION = "E_commers.asgi.application"  # ASGI for WebSockets

# ------------------------------------------------------------------
# Database
# ------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ------------------------------------------------------------------
# Channels (Real-time WebSocket configuration)
# ------------------------------------------------------------------
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ------------------------------------------------------------------
# Auth
# ------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.Account"
AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static & Media
# ------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "E_commers/static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------
# Messages
# ------------------------------------------------------------------
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# ------------------------------------------------------------------
# Email
# ------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = f"BuyTogether <{EMAIL_HOST_USER}>"
EMAIL_SUBJECT_PREFIX = "[BuyTogether] "

# ------------------------------------------------------------------
# Sessions
# ------------------------------------------------------------------
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True

# ------------------------------------------------------------------
# Security (enable when DEBUG=False)
# ------------------------------------------------------------------
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ------------------------------------------------------------------
# Custom app settings
# ------------------------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

REFERRAL_CODE_LENGTH = 10
MAX_PROFILE_IMAGE_SIZE = 1024 * 1024  # 1MB
ALLOWED_PROFILE_IMAGE_TYPES = ["image/jpeg", "image/png"]

CART_SESSION_ID = "cart"
ORDER_STATUS_CHOICES = [
    ("New", "New"),
    ("Accepted", "Accepted"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
]

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"}},
    "handlers": {
        "file": {"level": "DEBUG", "class": "logging.FileHandler", "filename": BASE_DIR / "debug.log", "formatter": "verbose"},
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console", "file"], "level": "INFO"},
}

# ------------------------------------------------------------------
# Razorpay keys from .env
# ------------------------------------------------------------------
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_hY56idBaXn2QQL")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "EssUCIZ4LHWzxDRF6J4U5azO")