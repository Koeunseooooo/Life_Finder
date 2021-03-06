"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$%o)p2&#2*v=^qp$tk^z+rpte5($uzs$m$!o3zzu%#6u(!tl=e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'cal',
    'main',
    'create_profile',
    'django.forms',

    'multiselectfield',
    'photo',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # provider
    'allauth.socialaccount.providers.google',

    'django_summernote',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True

USE_L10N = True

# USE_TZ = False
# DJANGO_CELERY_BEAT_TZ_AWARE = False


USE_TZ = True
# USE_TZ = False로 하면 이벤트를 저장할 때 한국 시간이 객체에 저장되지만
# SQLite backend does not support timezone-aware datetimes when USE_TZ is False.라는 오류 발생

# USE_TZ = True로 하면 9시간 이른 다른 나라 시간이 객체에 저장되지만 datetime을 사용해 객체를 불러와 가공한 차트는 보임
# 차트는 주로 객체 불러올 때 datetime을 사용했음 ex from datetime import datetime, date





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR,'static'),
# ]

#
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',
 'allauth.account.auth_backends.AuthenticationBackend',)

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SITE_ID = 1

# LOGIN_REDIRECT_URL = '/' ### 오류가 나면 홈으로 돌아와라
LOGIN_REDIRECT_URL = '/create/login_success'


# 이렇게하면 모든 뷰에 하나하나 today_date라는 변수를 안 넘겨줘도 된다
TEMPLATES[0]['OPTIONS']['context_processors'].append("cal.views.give_today_date")
TEMPLATES[0]['OPTIONS']['context_processors'].append("main.views.base")



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yaho.piro13@gmail.com'
EMAIL_HOST_PASSWORD = 'fgqizttebbnuutcj'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Yaho Team <noreply@Yaho.com>'
