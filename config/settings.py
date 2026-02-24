"""
Django settings for config project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# .env нужен локально, на Render обычно переменные задаются в панели
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except Exception:
    pass


# =========================
# CORE
# =========================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-unsafe-secret")
DEBUG = os.getenv("DEBUG", "0") == "1"

# Разрешаем Render поддомены + локалку, плюс добавляем вручную из env
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]

env_hosts = os.getenv("ALLOWED_HOSTS", "")
if env_hosts:
    ALLOWED_HOSTS += [h.strip() for h in env_hosts.split(",") if h.strip()]

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


# =========================
# APPS
# =========================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "clinic",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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
    }
]

WSGI_APPLICATION = "config.wsgi.application"


# =========================
# DATABASE
# =========================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =========================
# I18N
# =========================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# =========================
# CORS
# =========================
# Локально удобно открыть всем, на проде лучше ограничить домены фронта.
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    # Можно задать через переменную окружения, чтобы не править код
    env_cors = os.getenv("CORS_ALLOWED_ORIGINS", "")
    if env_cors:
        CORS_ALLOWED_ORIGINS = [o.strip() for o in env_cors.split(",") if o.strip()]
    else:
        # временно (потом поменяем на твой домен)
        CORS_ALLOWED_ORIGINS = [
            "https://kamilovsclinic.uz",
            "https://www.kamilovsclinic.uz",
        ]


# =========================
# STATIC
# =========================

STATIC_URL = "static/"


# =========================
# DEFAULT PK
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"