import os
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load .env variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security & Debug
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-placeholder")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'xray-backend-391z.onrender.com',  # Your backend Render URL
]

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    'django_filters',
    
    # Optional, comment out if Elasticsearch causes trouble
    'django_elasticsearch_dsl',

    'scans',  # your app
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xray_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'xray_project.wsgi.application'

# Database (SQLite for now)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ Optional Elasticsearch block – disable if it's not connected yet
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.getenv("ES_HOST", "https://localhost:9200"),
        'http_auth': (
            os.getenv("ES_USER", "elastic"),
            os.getenv("ES_PASS", "your-password")
        ),
        'verify_certs': False,
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ✅ Cloudinary Media files
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}

# CORS for frontend on Render/Netlify/etc
CORS_ALLOW_ALL_ORIGINS = True

# DRF
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
