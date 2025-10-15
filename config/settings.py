# settings.py

from pathlib import Path
import os
import dj_database_url  # Import dj_database_url

# BASE_DIR and environment variable setup remains the same
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # For development with whitenoise
    'django.contrib.staticfiles',
    # ... your other apps
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
    'rosetta',
    'django_jalali',
    'jalali_date',
    'accounts',
    'shop',
    'cart',
    'orders',
    'pages',
    'persian_translate',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add whitenoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'cart.context_processors.cart_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration for Render
DATABASES = {
    'default': dj_database_url.config(
        # Fallback to a local SQLite database if DATABASE_URL is not set
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation (remains the same)
# ...

# Internationalization (remains the same)
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
LANGUAGES = (('en', 'English'), ('fa', 'Persian'),)
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images) for production on Render
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Whitenoise storage configuration for optimal performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type (remains the same)
# ...

# Your other settings (AUTH_USER_MODEL, LOGIN_REDIRECT_URL, etc.) remain the same
# ...

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = 'shop:product_list'
LOGOUT_REDIRECT_URL = 'shop:product_list'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*']
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_UNIQUE_EMAIL = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}