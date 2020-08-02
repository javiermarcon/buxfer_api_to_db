
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# buxfer api
# settings to enter the buxfer api
BUXFER_CONN = {
    'max_retiries': 5,
    'url': 'https://www.buxfer.com/api',
    'user': '',
    'pass': ''
}


