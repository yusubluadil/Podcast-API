from .base import *


DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.parent / 'static']
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')
