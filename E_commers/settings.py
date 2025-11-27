# """
# Django settings for E_commers project.
# """

# from pathlib import Path
# import os
# from django.contrib.messages import constants as messages
# from dotenv import load_dotenv
# import dj_database_url

# # ------------------------------------------------------------------
# # Base Config
# # ------------------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Load .env variables
# load_dotenv(BASE_DIR / ".env")

# SECRET_KEY = os.getenv("SECRET_KEY", "local-secret-insecure")
# DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# # ✅ Better ALLOWED_HOSTS
# ALLOWED_HOSTS = [
#     "buytogether-1.onrender.com",
#     "127.0.0.1",
#     "localhost",
# ]

# # ✅ VERY IMPORTANT for 403 CSRF on Render (HTTPS)
# CSRF_TRUSTED_ORIGINS = [
#     "https://buytogether-1.onrender.com",
#     "https://*.onrender.com",
# ]

# # ------------------------------------------------------------------
# # Installed Apps
# # ------------------------------------------------------------------
# INSTALLED_APPS = [
#     "daphne",  # must be above Django for ASGI

#     # Django default apps
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "django.contrib.humanize",

#     # Third-party apps
#     "crispy_forms",
#     "crispy_bootstrap5",
#     "channels",

#     # Local apps
#     "E_commers",
#     "accounts",
#     "category",
#     "store",
#     "carts",
#     "orders",
#     "realtime",
# ]

# CRISPY_TEMPLATE_PACK = "bootstrap5"
# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# # ------------------------------------------------------------------
# # Middleware
# # ------------------------------------------------------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "whitenoise.middleware.WhiteNoiseMiddleware",  # Required for Render
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "E_commers.urls"

# # ------------------------------------------------------------------
# # Templates
# # ------------------------------------------------------------------
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [
#             BASE_DIR / "E_commers/templates",
#             BASE_DIR / "accounts/templates",
#             BASE_DIR / "store/templates",
#             BASE_DIR / "realtime/templates",
#         ],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#                 "category.context_processors.menu_links",
#                 "carts.context_processors.counter",
#                 "accounts.context_processors.user_profile",
#             ],
#         },
#     },
# ]

# # ------------------------------------------------------------------
# # ASGI & WSGI
# # ------------------------------------------------------------------
# ASGI_APPLICATION = "E_commers.asgi.application"
# WSGI_APPLICATION = "E_commers.wsgi.application"

# # ------------------------------------------------------------------
# # Database (Auto uses PostgreSQL on Render)
# # ------------------------------------------------------------------
# DATABASES = {
#     "default": dj_database_url.parse(
#         os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR/'db.sqlite3'}"),
#         conn_max_age=600,
#     )
# }

# # ------------------------------------------------------------------
# # Channels WebSocket Layer
# # ------------------------------------------------------------------
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }

# # ------------------------------------------------------------------
# # Auth
# # ------------------------------------------------------------------
# AUTH_USER_MODEL = "accounts.Account"

# AUTHENTICATION_BACKENDS = [
#     "accounts.backends.EmailBackend",
#     "django.contrib.auth.backends.ModelBackend",
# ]

# # ------------------------------------------------------------------
# # Password Validation
# # ------------------------------------------------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# # ------------------------------------------------------------------
# # Localization
# # ------------------------------------------------------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "Asia/Kolkata"
# USE_I18N = True
# USE_TZ = True

# # ------------------------------------------------------------------
# # Static & Media
# # ------------------------------------------------------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [BASE_DIR / "E_commers/static"]

# # ✅ Tell Django to use Whitenoise's storage in production
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # ------------------------------------------------------------------
# # Security cookies (good for HTTPS on Render)
# # ------------------------------------------------------------------
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# # ------------------------------------------------------------------
# # Messages
# # ------------------------------------------------------------------
# MESSAGE_TAGS = {
#     messages.DEBUG: "alert-info",
#     messages.INFO: "alert-info",
#     messages.SUCCESS: "alert-success",
#     messages.WARNING: "alert-warning",
#     messages.ERROR: "alert-danger",
# }

# # ------------------------------------------------------------------
# # Email
# # ------------------------------------------------------------------
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
# DEFAULT_FROM_EMAIL = f"BuyTogether <{EMAIL_HOST_USER}>"

# # ------------------------------------------------------------------
# # Razorpay Keys
# # ------------------------------------------------------------------
# RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_hY56idBaXn2QQL")
# RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "EssUCIZ4LHWzxDRF6J4U5azO")

"""
Django settings for E_commers (BuyTogether) project.
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages
from dotenv import load_dotenv
import dj_database_url

# ------------------------------------------------------------------
# Base Config
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env variables
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "local-secret-insecure")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Allowed Hosts
ALLOWED_HOSTS = [
    "*",
    "127.0.0.1",
    "localhost",
    "buytogether-1.onrender.com",
]

# CSRF Trusted
CSRF_TRUSTED_ORIGINS = [
    "https://buytogether-1.onrender.com",
    "https://*.onrender.com",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ------------------------------------------------------------------
# Installed Apps
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "daphne",  # must be above Django for ASGI

    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",
    "channels",

    # Local apps
    "E_commers",
    "accounts",
    "category",
    "store",
    "carts",
    "orders",
    "realtime",
]

CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # for Render static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "E_commers.urls"

# ------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "E_commers/templates",
            BASE_DIR / "accounts/templates",
            BASE_DIR / "store/templates",
            BASE_DIR / "realtime/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "category.context_processors.menu_links",
                "carts.context_processors.counter",
                "accounts.context_processors.user_profile",
            ],
        },
    },
]

# ------------------------------------------------------------------
# ASGI + WSGI
# ------------------------------------------------------------------
ASGI_APPLICATION = "E_commers.asgi.application"
WSGI_APPLICATION = "E_commers.wsgi.application"

# ------------------------------------------------------------------
# Database / Render PostgreSQL + Local SQLite
# ------------------------------------------------------------------
if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.parse(os.getenv("DATABASE_URL"), conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ------------------------------------------------------------------
# Channels Layer
# ------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# ------------------------------------------------------------------
# Auth
# ------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.Account"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# ------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------
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

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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
# ------------------------------------------------------------------
# Razorpay Keys
# ------------------------------------------------------------------
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_hY56idBaXn2QQL")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "EssUCIZ4LHWzxDRF6J4U5azO")
