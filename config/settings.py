"""
Django settings for config project.
"""

import os
from pathlib import Path
import dj_database_url
from django.contrib.messages import constants as message_constants

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-3z@3($(#x9tt36x*i^eeb3%sx*1@!h@m2gw&m=27(#obx1sr8z",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "ecommerce-m7.onrender.com"]

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8000",
    "http://localhost:8000",
    "https://127.0.0.1:8000",
    "http://127.0.0.1:8000",
    "https://ecommerce-m7.onrender.com",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "cloudinary_storage",
    "cloudinary",
    "tienda",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
        "DIRS": [BASE_DIR / "tienda" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "tienda.context_processors.carrito_info",
                "tienda.context_processors.categorias_globales",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Override with PostgreSQL when DATABASE_URL is set (production)
if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.parse(
        os.environ["DATABASE_URL"], conn_max_age=600
    )


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media"))

cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
if cloud_name:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": cloud_name,
        "API_KEY": os.environ.get("CLOUDINARY_API_KEY", ""),
        "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", ""),
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": "wf4xjrci",
        "API_KEY": "481984371727142",
        "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", ""),
    }

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

MESSAGE_TAGS = {
    message_constants.DEBUG: "secondary",
    message_constants.ERROR: "danger",
}
