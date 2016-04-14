# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

# Add apps to the PYTHON PATH
sys.path.insert(0, root('apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1$s^ggnnc16*_9=a^5yv3jr4pw3a=f##c#fc!ewc&i5n^q88l%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'dc_theme',
    'static_precompiler',
    'elections',
    'markdown_deux',
    'core',
    'notifications',
    'people',
    'mentions',
    'parties',
    # 'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.UTMTrackerMiddleware',
)

ROOT_URLCONF = 'wcivf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dc_theme.context_processors.dc_theme_context',
                'core.context_processors.canonical_url',
                'core.context_processors.use_compress_css',
                'core.context_processors.postcode_form',
                'dealer.contrib.django.context_processor',
            ],
        },
    },
]

USE_COMPRESSED_CSS = False
MEDIA_ROOT = root('media')
MEDIA_URL = "/media/"

WSGI_APPLICATION = 'wcivf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    root('assets'),
    root('static'),
)
# STATIC_ROOT = root('static_root')

# TODO find a way to move these in to the DC theme app?
STATIC_PRECOMPILER_ROOT = root('static')
import os
import dc_theme
root_path = os.path.dirname(dc_theme.__file__)
STATIC_PRECOMPILER_COMPILERS = (
    ('static_precompiler.compilers.scss.SCSS', {
        "sourcemap_enabled": True,
        # "output_style": "compressed",
        "load_paths": [
            root_path + '/static/dc_theme/bower_components/foundation-sites/assets',
            root_path + '/static/dc_theme/bower_components/foundation-sites/scss',
            root_path + '/static/dc_theme/bower_components/motion-ui/src',
            root_path + '/static/dc_theme/scss/',
        ],
    }),
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

YNR_BASE = "https://candidates.democracyclub.org.uk"
CANONICAL_URL = "https://whocanivotefor.co.uk"

SITE_TITLE = "Who Can I Vote For?"

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass
