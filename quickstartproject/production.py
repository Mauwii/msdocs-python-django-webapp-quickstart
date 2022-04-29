from .settings import *
import sys
import os

DEBUG = False

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

# WhiteNoise configuration
MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
# Add whitenoise middleware after the security middleware                             
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',                    
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

APPLICATIONINSIGHTS_CONNECTION_STRING = os.environ['APPLICATIONINSIGHTS_CONNECTION_STRING']

LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
    "handlers": {
        "azure": {
            "level": "DEBUG",
            "class": "opencensus.ext.azure.log_exporter.AzureLogHandler",
            "connection_string": APPLICATIONINSIGHTS_CONNECTION_STRING,
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "djangologger": {
            "handlers": [
                "azure",
                "console"
            ]
        },
    },
}
