import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'heePhe4AZaiG1Aiy'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'obican', 'templates'),
                os.path.join(BASE_DIR, 'core', 'templates')],
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

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

ROOT_URLCONF = 'debits.debits_test.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

## debits settings

PAYMENTS_HOST = 'https://debits.job-lab.net'
IPN_HOST = 'https://debits.job-lab.net'
FROM_EMAIL = 'admins@arcamens.com'
PROLONG_PAYMENT_VIEW = 'transaction-prolong-payment'
PAYMENTS_DAYS_BEFORE_DUE_REMIND = 10
PAYMENTS_DAYS_BEFORE_TRIAL_END_REMIND = 10
PAYPAL_EMAIL = 'paypal-sandbox-merchant@portonvictor.org'
PAYPAL_ID = 'CDA2QQH9TQ44C' #PayPal account ID
# https://developer.paypal.com/developer/applications
PAYPAL_CLIENT_ID = 'AVV1uyNk5YCJfDaDgUI9QwsYCtyEP8aFyMV7pCaiUn7Icuo8TYwaaXDM2nTV25wEGKHMl2CAeT4XD9BR'
PAYPAL_SECRET = 'EAoz5-mhOlLAUIfcyxAflcx2Tr7EHkEzm998ayh1ntbfZrk56IeQP9f3wJSd3WCAJss0rtYh67eI-CDs'
PAYPAL_DEBUG = True
PAYMENTS_REALM = 'testapp30'

#DEBUG_PROPAGATE_EXCEPTIONS = True

#SQL_STACKTRACE = True
#LOGGING = {
#    'version': 1,
#    'filters': {
#        'require_debug_true': {
#            '()': 'django.utils.log.RequireDebugTrue',
#        }
#    },
#    'handlers': {
#        'console': {
#            'level': 'DEBUG',
#            'filters': ['require_debug_true'],
#            'class': 'logging.StreamHandler',
#        }
#    },
#    'loggers': {
#        'django.db.backends': {
#            'level': 'DEBUG',
#            'handlers': ['console'],
#        }
#    }
#}
