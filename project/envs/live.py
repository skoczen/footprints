import os
from memcacheify import memcacheify
from postgresify import postgresify
from envs.common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG
BASE_URL = "https://www.footprintsapp.com"
# PREPEND_WWW = True

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = os.environ['MAILGUN_API_KEY']
MAILGUN_SERVER_NAME = 'mg.footprintsapp.com'
BROKER_URL = os.environ["REDISTOGO_URL"]

MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL
COMPRESS_URL = STATIC_URL
FAVICON_URL = "%sfavicon.ico" % STATIC_URL

CACHES = memcacheify()
DATABASES = None
DATABASES = postgresify()
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = "backends.CachedS3BotoStorage"
COMPRESS_STORAGE = STATICFILES_STORAGE

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get("GOOGLE_ANALYTICS_PROPERTY_ID", "")
INTERCOM_APP_ID = os.environ.get('INTERCOM_APP_ID', "")
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
