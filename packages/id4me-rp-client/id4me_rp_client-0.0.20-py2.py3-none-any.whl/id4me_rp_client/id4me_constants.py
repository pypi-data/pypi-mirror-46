__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 IONOS SE"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"


from enum import Enum


class OIDCScope(Enum):
    openid = 'openid'
    profile = 'profile'
    email = 'email'
    address = 'address'
    phone = 'phone'
    offline_access = 'offline_access'

    def __str__(self):
        return self.value


class OIDCApplicationType(Enum):
    web = 'web'
    native = 'native'

    def __str__(self):
        return self.value


class OIDCPrompt(Enum):
    none = 'none'
    login = 'login'
    consent = 'consent'
    login_and_consent = 'login consent'
    selectaccount = 'select_account'
    selectaccount_and_login = 'select_account login'
    selectaccount_and_consent = 'select_account consent'
    selectaccount_and_login_and_consent = 'select_account login consent'

    def __str__(self):
        return self.value


class OIDCClaim(Enum):
    sub = 'sub'
    name = 'name'
    given_name = 'given_name'
    family_name = 'family_name'
    middle_name = 'middle_name'
    nickname = 'nickname'
    preferred_username = 'preferred_username'
    profile = 'profile'
    picture = 'picture'
    website = 'website'
    email = 'email'
    email_verified = 'email_verified'
    gender = 'gender'
    birthdate = 'birthdate'
    zoneinfo = 'zoneinfo'
    locale = 'locale'
    phone_number = 'phone_number'
    phone_number_verified = 'phone_number_verified'
    address = 'address'
    updated_at = 'updated_at'

    def __str__(self):
        return self.value


class ID4meClaim(Enum):
    pass
