__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 IONOS SE"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"


class ID4meException(Exception):
    def __init__(self, message):
        self.message = message
        pass

class ID4meInvalidIDException(ID4meException):
    pass

class ID4meDNSResolverException(ID4meException):
    pass


class ID4meDNSSECException(ID4meException):
    pass


class ID4meAuthorityConfigurationException(ID4meException):
    pass


class ID4meRelyingPartyRegistrationException(ID4meException):
    pass


class ID4meTokenRequestException(ID4meException):
    pass

class ID4meTokenException(ID4meException):
    pass

class ID4meUserInfoRequestException(ID4meException):
    pass
