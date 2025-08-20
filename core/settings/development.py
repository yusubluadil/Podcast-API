from .base import *


DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.parent / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')

INTERNAL_IPS = [
    '127.0.0.1',
]
