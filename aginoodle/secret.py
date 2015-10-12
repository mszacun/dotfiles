

SECRET_KEY = '3183a1818da771e70f604e31a0ead60dc36b5afa' # put your secret key here

# put your database connection settings here
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aginoodle',
        'USER': 'aginoodle',
        'PASSWORD': 'asdf',

        'HOST': 'localhost',
        'PORT': '',

    }
}

from backlog.settings.common import INSTALLED_APPS
INSTALLED_APPS += (
      'django_extensions',
       )

SHELL_PLUS_PRE_IMPORTS = (
    ('backlog.tests.utils.data_creators', '*'),
    ('pprint', 'pprint'),
)

import ldap
from django_auth_ldap.config import LDAPSearch

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = "ldaps://ed-p-gl.emea.nsn-net.net"

AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("o=NSN",
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {"email": "mail"}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
HOST_URL = 'http://localhost:8000'

TEAMCAL_DB = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'teamcal',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': 'localhost'
}
