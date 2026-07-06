"""
Django settings - OPTIMIZED FOR SPEED
"""

from pathlib import Path
import os
import sys
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

def env_list(key: str, default: str = ""):
    val = os.getenv(key, default)
    return [x.strip() for x in val.split(",") if x.strip()]

DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes", "on")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

# Key used to encrypt/decrypt the staff-recoverable copy of user passwords
# (see accounts/crypto.py). Falls back to a key derived from SECRET_KEY for
# local development only — set a real PASSWORD_RECOVERY_KEY in production.
import base64
import hashlib
PASSWORD_RECOVERY_KEY = os.getenv("PASSWORD_RECOVERY_KEY") or base64.urlsafe_b64encode(
    hashlib.sha256(SECRET_KEY.encode()).digest()
).decode()

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,.ondigitalocean.app,ilendlending.com,www.ilendlending.com"
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost,http://127.0.0.1,https://*.ondigitalocean.app,https://ilendlending.com,https://www.ilendlending.com"
)

INSTALLED_APPS = [
    "staffdash",
    "cloudinary",
    "jazzmin",
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "django.contrib.humanize",
]

# ✅ OPTIMIZED MIDDLEWARE - NO CACHE MIDDLEWARE (causes slowness)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "accounts.middleware.PortalSessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'accounts.middleware.CheckUserActiveMiddleware',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ✅ DATABASE
_db_url = (
    os.getenv("PUBLIC_DATABASE_URL")
    or os.getenv("DATABASE_URL")
    or ""
).strip()

_db_url_is_valid = "://" in _db_url and bool(_db_url.split("://", 1)[0])

# DigitalOcean App Platform does not inject database-binding env vars
# (${db.DATABASE_URL}) during the BUILD phase, only at runtime — so the
# buildpack's automatic `collectstatic` step (which never touches the
# database) always sees an empty DATABASE_URL. Allow the harmless SQLite
# fallback there; every other command (migrate, gunicorn/wsgi, shell, ...)
# actually needs the real database, so it still fails loudly if misconfigured.
_is_collectstatic = len(sys.argv) > 1 and sys.argv[1] == "collectstatic"

if not _db_url_is_valid:
    if DEBUG or _is_collectstatic:
        # Local dev convenience / build-time collectstatic only. NEVER let
        # this silently happen for migrate or the running server — that's
        # what wiped the production users table (DATABASE_URL pointed at a
        # component name that didn't exist, so the app quietly ran on a
        # throwaway SQLite file that resets on every deploy).
        _db_url = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    else:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            f"DATABASE_URL is missing or did not resolve to a real connection "
            f"string (got: {_db_url!r}). Refusing to silently fall back to "
            f"SQLite in production. Fix the DATABASE_URL environment variable "
            f"— it must reference the exact name of the attached database "
            f"component."
        )

DATABASES = {
    "default": dj_database_url.parse(_db_url, conn_max_age=0)
}

# PostgreSQL specific options (Production only)
if not DEBUG:
    db_engine = DATABASES["default"].get("ENGINE", "")
    if "postgresql" in db_engine:
        DATABASES["default"].setdefault("OPTIONS", {})
        DATABASES["default"]["OPTIONS"]["connect_timeout"] = 10

# ✅ CACHES - SIMPLE (No complex options)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/login/"

# ✅ STATIC FILES - OPTIMIZED
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# ✅ CSRF & UPLOAD
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20MB
FILE_UPLOAD_MAX_NUMBER_FILES = 10

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_MAX_AGE = 31536000

# ✅ CLOUDINARY
import cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", ""),
    api_key=os.getenv("CLOUDINARY_API_KEY", ""),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", ""),
    secure=True,
)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME", ""),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY", ""),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET", ""),
}

# ✅ SECURITY
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ✅ LOGGING - MINIMAL (for speed)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,  # Disable all loggers for speed
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",  # Only errors
            "propagate": False,
        },
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "Loan Admin",
    "site_header": "Loan Admin",
    "site_brand": "Loan Admin",
    "welcome_sign": "Welcome",
    "copyright": "Loan",
    "show_sidebar": True,
    "navigation_expanded": True,
    "theme": "darkly",
    "custom_css": "css/admin_custom.css",
}