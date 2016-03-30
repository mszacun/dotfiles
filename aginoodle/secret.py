
from backlog.settings.common import *


SITE_URL = ''
MEDIA_URL = SITE_URL + '/media/'
STATIC_URL = SITE_URL + '/static/'
LOGIN_REDIRECT_URL = SITE_URL + '/user/profile/'
LOGIN_URL = SITE_URL + '/user/login/'

MAINTENANCE_IGNORE_URLS = (
    r'^%s/accounts/login/.*' % SITE_URL,
    r'^%s/accounts/logout/.*' % SITE_URL,
    r'^%s/admin/.*' % SITE_URL,
)


SECRET_KEY = '3183a1818da771e70f604e31a0ead60dc36b5afa'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SESSION_COOKIE_NAME = 'aginoodleDevSessionId'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


LOGIN_REQUIRED_URLS = (
    SITE_URL + '/features/',
    SITE_URL + '/items/',
    SITE_URL + '/sprints/',
    SITE_URL + '/teams/',
    SITE_URL + '/account/',
)




DATABASES = {
    'default':
    {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aginoodle',
        'USER': 'aginoodle',
        'PASSWORD': 'Acizie4n',
        'HOST': 'localhost',
        'PORT': '',
    },

}

TEAMCAL_DB = [{
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'teamcal',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': 'localhost'
}]

ENABLED_FEATURES = {
    'capacity': True,
    'feature_hierarchy': True,
    'feature_id_dash_delimited': True
}

from backlog.settings.common import INSTALLED_APPS
INSTALLED_APPS += (
    'django_extensions',
)

SHELL_PLUS_PRE_IMPORTS = (
    ('backlog.tests.utils.data_creators', '*'),
    ('pprint', 'pprint'),
    ('reversion', '*'),
)
