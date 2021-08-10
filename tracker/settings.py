import os
import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.getenv("DATA_DIR", BASE_DIR)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    secret_path = os.path.join(DATA_DIR, "secret.key")
    if os.path.exists(secret_path):
        SECRET_KEY = open(secret_path, "r").read().strip()
    else:
        with open(os.path.join(DATA_DIR, "secret.key"), "w") as f:
            SECRET_KEY = secrets.token_hex(32)
            f.write(SECRET_KEY)

DEBUG = os.getenv("DEBUG", "true") == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tracker",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tracker.urls"

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

WSGI_APPLICATION = "tracker.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(DATA_DIR, "db.sqlite3"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, "static"))

# Remove tracked games that have not been seen for this many seconds.
TRACKER_PRUNE_SECONDS = int(os.getenv("TRACKER_PRUNE_SECONDS", 60))
TRACKER_DISCORD_WEBHOOK = os.getenv("TRACKER_DISCORD_WEBHOOK")
TRACKER_DISCORD_ROLE_ID = os.getenv("TRACKER_DISCORD_ROLE_ID")
TRACKER_DISCORD_NOTIFY_PASSWORDED = (
    os.getenv("TRACKER_DISCORD_NOTIFY_PASSWORDED", "false") == "true"
)
