


import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"


ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', 'localhost')]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'widget_tweaks',
    
    # Local apps
    'accounts.apps.AccountsConfig',
    'tools.apps.ToolsConfig',
    'bookings.apps.BookingsConfig',
    'reports.apps.ReportsConfig',
    'core.apps.CoreConfig',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'toolhire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Global template directory (optional)
            os.path.join(BASE_DIR, 'templates'),
            # App-specific template directory
            os.path.join(BASE_DIR, 'accounts', 'templates'),
            os.path.join(BASE_DIR, 'tools', 'templates'),
            os.path.join(BASE_DIR, 'bookings', 'templates'),
            os.path.join(BASE_DIR, 'reports', 'templates'),
            os.path.join(BASE_DIR, 'core', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'toolhire.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_REDIRECT_URL = '/accounts:dashboard'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Stripe settings
STRIPE_PUBLIC_KEY = 'pk_test_51RF8Qg4fsNGmT5PiYfWD9VyLwOtJtKez5HHstep4h631nQs98oVRxEthYbFB3QKspwUURM0z2Vcau58vrpF3vyaN00FbUuelAd'
STRIPE_SECRET_KEY = 'sk_test_51RF8Qg4fsNGmT5PiLlT64QiXrpzO7F83qdYfbywV0bjDrQQVa09QXCGNjYECk2B1IKsrQYGxjfkfdxe2R5Iz7YLz00ZAtw0xiF'

# Additional configurations
# Ensure that the static files directory exists to avoid warnings.
# Make sure the directories exist as specified for static and media files.
LOGIN_REDIRECT_URL = 'dashboard'
