"""
Base settings to build other settings files upon.
"""
from __future__ import absolute_import, unicode_literals

import os
import mimetypes
from pathlib import Path

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _


import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# radio_funk/
APPS_DIR = ROOT_DIR / "radio_funk"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
PRODUCTION = env.bool("PRODUCTION", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "America/New_York"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LANGUAGES = (
    ('af', _('African')),
    ('ar', _('Arabic')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
)
PARLER_LANGUAGES = {
    None: (
        {'code': 'af',}, # African
        {'code': 'ar',}, # Arabic
        {'code': 'en',}, # English
        {'code': 'es',}, # Spanish
        {'code': 'fr',}, # French
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger'
}

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL", default="postgis:///radio_funk"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'leaflet',

    # 'jet.dashboard',
    # 'jet',

    "admin_honeypot",

    "tinymce",
    "filebrowser",

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Handy template tags
    "django.contrib.admin",
    "django.contrib.admindocs",
    'django.contrib.gis',
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    "django_celery_beat",

    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",

    "tailwind",
    "theme",

    'django_social_share',

    # image resize automatic
    'stdimage',

    'countries_plus',

    'rosetta',
    'parler',

    # IP Address and Location
    'geoip2',
    # Get User phone details from IP
    'django_user_agents',

    # reactive django
    'django_unicorn',

    # photo gallery
    # 'photologue',
    # 'sortedm2m',

    'django_browser_reload'
]

LOCAL_APPS = [
    "radio_funk.users",
    "radio_funk.genre",
    "radio_funk.tunes",
    "radio_funk.mode",
    "radio_funk.podcast",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "radio_funk.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# https://amalshaji.com/blog/django-magic-link/
#  Magic Link Setup
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
LOGOUT_REDIRECT_URL = "home"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    # HTML Minifying
    "django.middleware.gzip.GZipMiddleware",
    'django.middleware.cache.UpdateCacheMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',

    # Django Default Middlewares
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',

    'django_user_agents.middleware.UserAgentMiddleware',

    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"
ADMIN_MEDIA_PREFIX = "/admin/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "radio_funk.utils.context_processors.context_data",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "SAMEORIGIN"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 500
APPEND_SLASH = True

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "portal/"
ADMIN_DOC_URL = "portal/doc/"
ADMIN_FILEBROWSER_URL = "portal/filebrowser/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Webmaster""", "noreply@radiofunk.io"), ("""Developer""", "info@darkcodr.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="pyamqp://guest@localhost")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="db+sqlite:///results.sqlite")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 600
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_OLD_PASSWORD_FIELD_ENABLED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "radio_funk.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
ACCOUNT_FORMS = {"signup": "radio_funk.users.forms.UserSignupForm"}
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "radio_funk.users.adapters.SocialAccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
SOCIALACCOUNT_FORMS = {"signup": "radio_funk.users.forms.UserSocialSignupForm"}
SOCIALACCOUNT_QUERY_EMAIL = True
# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# By Default swagger ui is available only to admin user. You can change permission classs to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "radio_funk API",
    "DESCRIPTION": "Documentation of API endpoiints of radio_funk",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SERVERS": [
        {"url": "https://127.0.0.1:8000", "description": "Local Development server"},
        {"url": "https://radiofunk.io", "description": "Production server"},
    ],
}
# Your stuff...
# ------------------------------------------------------------------------------
# minifying django HTML Files
HTML_MINIFY = True
EXCLUDE_FROM_MINIFYING = ('^jet/', '^admin/', '^tinymce/', '^filebrowser/')
KEEP_COMMENTS_ON_MINIFYING = True

# https://django-tailwind.readthedocs.io/en/latest/installation.html
# Working with tailwindcss in django
TAILWIND_APP_NAME = 'theme'

# https://github.com/smacker/django-filebrowser-no-grappelli
FILEBROWSER_SHOW_IN_DASHBOARD = False
FILEBROWSER_DIRECTORY = "filebrowser/uploads/"
FILEBROWSER_NORMALIZE_FILENAME = False
FILEBROWSER_MAX_UPLOAD_SIZE = 26214400
FILEBROWSER_CONVERT_FILENAME = True
FILEBROWSER_FOLDER_REGEX = r'^[\w._\ /-]+$'
FILEBROWSER_VERSION_QUALITY = 90
FILEBROWSER_ADMIN_THUMBNAIL = "admin_thumbnail"
FILEBROWSER_VERSION_PROCESSORS = ["filebrowser.utils.scale_and_crop"]
FILEBROWSER_ADMIN_VERSIONS = ["thumbnail", "small", "medium", "big", "large"]

# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
FILE_UPLOAD_MAX_MEMORY_SIZE = 262144000  # i.e. 25.0 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 262144000  # i.e. 2.5 MB

# Maximum number of GET/POST parameters that will be read before a
# SuspiciousOperation (TooManyFieldsSent) is raised.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000


# Number Settings for human readable grouping style and comma
# Decimal separator symbol
DECIMAL_SEPARATOR = "."
# Boolean that sets whether to add thousand separator when formatting numbers
USE_THOUSAND_SEPARATOR = True

# Thousand separator symbol
THOUSAND_SEPARATOR = ","

# Number of digits that will be together, when splitting them by
# THOUSAND_SEPARATOR. 0 means no grouping, 3 means splitting by thousands...
NUMBER_GROUPING = 3

# JET_CHANGE_FORM_SIBLING_LINKS = True
# TODO: Add google analytics client_secret file
# JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = (str(APPS_DIR / "client_secrets.json"),)
JET_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultIndexDashboard'
JET_APP_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultAppIndexDashboard'
JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

# Tiny MCE Config
TINYMCE_DEFAULT_CONFIG = {
    "selector": "textarea",
    "height": "260px",
    "width": "80%",
    'theme':'modern',
    'statusbar':'True',
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "en",  # To force a specific language instead of the Django current language.
}
# TINYMCE_SPELLCHECKER = True
# TINYMCE_COMPRESSOR = True

# GOOGLE_CLIENT_ID = env('GOOGLE_CLIENT_ID')
# GOOGLE_CLIENT_SECRET = env('GOOGLE_CLIENT_SECRET')

# RADIO_API = env("RADIO_API")
# RADIO_HOST = env("HOST")

MAPBOX_KEY = env("MAPBOX_KEY")

NPM_BIN_PATH = '/usr/local/bin/npm'
GEOIP_PATH = str(ROOT_DIR / "geoip")

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'openid',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
            'prompt': 'consent',
            'response_type': 'code'
        }
    },
    'facebook': {
        'SCOPE': [
            'profile',
            'email',
            'openid',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
            'prompt': 'consent',
            'response_type': 'code'
        }
    }
}

PODCASTING_IMG_PATH = "img"
PAGINATE_BY = 10
FEED_ENTRIES = None

