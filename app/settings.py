import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-watl^4)7r+oh7-vw)4qg#m3j=5g61we@ij3h#n)e-j8z8^gy(v'
DEBUG = True

ALLOWED_HOSTS = [
    "72.60.59.58",
    "agendavip.shop",
    "www.agendavip.shop",
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'agendavip',
    'app',
    'cart',
    'events',
    'payments',
    'tickets',
    'django_countries',
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agendavip_sigma',
        'USER': 'agendavip_sigma',
        'PASSWORD': '4F:+>XLa@&)F3Wk',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.User"

# Mercado Pago - Ambiente de Teste
import os
from decouple import config

# 🔑 Credenciais do Mercado Pago (produção)
MERCADOPAGO_PUBLIC_KEY = config(
    "MERCADOPAGO_PUBLIC_KEY",
    default="APP_USR-03d984a5-ed33-4bb6-9ee5-489a647b0ec3"
)

MERCADOPAGO_ACCESS_TOKEN = config(
    "MERCADOPAGO_ACCESS_TOKEN",
    default="APP_USR-6124180248187430-090213-25a88846779d409af3d021dc41e7c6c4-588904921"
)

MERCADOPAGO_CLIENT_ID = config(
    "MERCADOPAGO_CLIENT_ID",
    default="6124180248187430"
)

MERCADOPAGO_CLIENT_SECRET = config(
    "MERCADOPAGO_CLIENT_SECRET",
    default="bMaVCuRcCdYa6lfLJspZ60pF1XNDmkNg"
)

# 🔒 Secret que você já tinha configurado para Webhook
MERCADOPAGO_WEBHOOK_SECRET = config(
    "MERCADOPAGO_WEBHOOK_SECRET",
    default="9b877b24ae692fdfb4587d8b46fdeb11a517a116b08dae570f7b6da091895e6c"
)

# 🌐 URL em produção
PRODUCTION_URL = config(
    "PRODUCTION_URL",
    default="https://agendavip.shop"
)


LOGIN_URL = 'login' 