
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
SESSION_COOKIE_NAME = 'aginoodleDevSessionId'

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ALLOWED_HOSTS = ['localhost']
SERVER_EMAIL = 'do-not-reply.aginoodle@nokia.com'
DEFAULT_FROM_EMAIL = 'do-not-reply.aginoodle@nokia.com'
EMAIL_HOST = "mail.emea.nsn-intra.net"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
ADMINS = (('ja', 'marcin.szachun@nokia.com'), )



LOGIN_REQUIRED_URLS = (
    SITE_URL + '/features/',
    SITE_URL + '/items/',
    SITE_URL + '/sprints/',
    SITE_URL + '/teams/',
    SITE_URL + '/account/',
)

import ldap
from django_auth_ldap.config import LDAPSearch

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'backlog.aginoodle_shared.authentication_backends.StopCheckingPermissionsBackend',
    'django_auth_ldap.backend.LDAPBackend',
)
AUTH_LDAP_SERVER_URI = "ldap://ed-p-gl.emea.nsn-net.net"
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""

AUTH_LDAP_FIND_GROUP_PERMS = False
AUTH_LDAP_CACHE_GROUPS = False
AUTH_LDAP_CONNECTION_OPTIONS = {
        ldap.OPT_REFERRALS: 0
}

AUTH_LDAP_USER_SEARCH = LDAPSearch("o=NSN", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_USER_ATTR_MAP = {"email": "mail"}


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

TEAMCAL_DB = {}

ENABLED_FEATURES = {
    'capacity': True,
    'feature_hierarchy': True,
    'green_teams': True,
    'feature_id_dash_delimited': True
}

from backlog.settings.common import INSTALLED_APPS
INSTALLED_APPS += (
    'django_extensions',
)

SHELL_PLUS_PRE_IMPORTS = (
    ('backlog.tests.utils.data_creators', '*'),
    ('backlog.utils', '*'),
    ('pprint', 'pprint'),
    ('reversion.revisions', '*'),
)

DEFAULT_SPRINT_PLANNING_TEAM_NAME = 'FTW11'
