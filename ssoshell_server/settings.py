"""
Django settings for ssoshell_server project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import environ
import os

env = environ.Env(
    DEBUG=(bool, False)
)

LOGIN_REDIRECT_URL = '/success'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qo445$#w+(dz&1ynacytdc1w&42xo#06yg)+-n!+am(p^43*22'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env('APP_HOSTNAME', default=['*'])
# CSRF_TRUSTED_ORIGINS = "https://ca.ssosh.io"
CSRF_TRUSTED_ORIGINS = ['https://ca.ssosh.io']
AUTH_SERVER = env('OIDC_AUTH_SERVER')
AUTH_CLIENT_ID = env('OIDC_AUTH_CLIENT_ID')
AUTH_CLIENT_SECRET = env('OIDC_AUTH_CLIENT_SECRET')
AUTH_SCOPE = env('OIDC_AUTH_SCOPE', default="openid").split(",")

SSH_CA_CERT_PATH = env('SSH_CA_CERT_PATH', default='ssh_ca')
SSH_CA_CERT_PASSWORD = env('SSH_CA_CERT_PASSWORD', default='')
SSH_CA_ROTATION = env('SSH_CA_ROTATION', default=24)
SSH_CA_CERT_VALIDITY = env('SSH_CA_CERT_VALIDITY', default=8)
SSH_CA_CERT_SUBJECT_OIDC = env('SSH_CA_CERT_SUBJECT_OIDC', default='sub')
SSH_CA_CERT_SUBJECT_SAML = env('SSH_CA_CERT_SUBJECT_SAML', default='samaccountname')
SSH_CA_CERT_SUBJECT_BUILTIN = env('SSH_CA_CERT_SUBJECT_BUILTIN', default='username')

# Application definition

INSTALLED_APPS = [
    'ssoshell_server.user',
    'ssoshell_server.device_auth',
    'ssoshell_server.oidc_authentication',
    'ssoshell_server.ssh_ca',
    'ssoshell_server.host',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ssoshell_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ssoshell_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
