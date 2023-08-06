# id4me-rp-client
Python Relying Party client library for ID4me protocol.
For details of the protocol, please visit: https://id4me.org

Library offers Relying Party functionality for authentication with Identity Authority and claim request from the Identity Agent..

## Specification reference
https://gitlab.com/ID4me/documentation/blob/master/id4ME%20Technical%20Specification.adoc
- Version: 1.0
- Revision: 02

## Installation
```shell
pip install id4me-rp-client
```

## Usage

### Register the client and authorize with Identity Authority

```python
from id4me_rp_client import *

# these imports are just needed in this example
from builtins import input
import json

registrations = dict()

# a routine to save client registration at authority
def save_authority_registration(auth_name, auth_content):
    registrations[auth_name] = auth_content
    pass


# a routine to load client registration at authority
def load_authority_registration(auth_name):
    return registrations[auth_name]

# create client object with basic parameters of your app
client = ID4meClient(
    get_client_registration=load_authority_registration,
    save_client_registration=save_authority_registration,
    app_type=OIDCApplicationType.web,
    validate_url='https://dynamicdns.domainconnect.org/ddnscode',
    client_name='Foo app',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/7/76/Foobar2000_logo_2014.png',
    policy_url='https://foo.com/policy',
    tos_url='https://foo.com/tos',
    private_jwks_json=ID4meClient.generate_new_private_keys_set())

try:
    # make a discovery of identity authority and register if needed
    # find_authority and save_authority are optional, but when missing client will be registered each time anew
    ctx = client.get_rp_context(
        id4me='id200.connect.domains')    

    # get a link to login routine
    link = client.get_consent_url(
        ctx,
        claimsrequest=ID4meClaimsRequest(
            userinfo_claims={
                OIDCClaim.name: ID4meClaimRequestProperties(reason='To call you by name'),
                OIDCClaim.email: ID4meClaimRequestProperties(essential=True, reason='To be able to contact you'),
                OIDCClaim.email_verified: ID4meClaimRequestProperties(reason='To know if your E-mail was verified'),
            })
        )
    print('Please open the link:\n{}'.format(link))

    # Normally code will arrive as query param on client.validateUrl
    code = input('Please enter code: ')
    # Get ID token
    client.get_idtoken(context=ctx, code=code)
    # Get User Info
    userinfo = client.get_user_info(context=ctx)
    print('User Info:\n{}'.format(json.dumps(userinfo, sort_keys=True, indent=4)))    
except ID4meException as e:
    print('Exception: {}'.format(e))

```

#### Output:
```text
Resolving "_openid.id200.connect.domains."
Checking TXT record "v=OID1;iss=id.test.denic.de;clp=identityagent.de"
identity_authority = auth.freedom-id.de
registering with new identity authority (auth.freedom-id.de)
destination = https://auth.freedom-id.de/login?scope=openid&response_type=code&client_id=hmkzay2riyon4&redirect_uri=https%3A//foo.com/validate&login_hint=id200.connect.domains&state=&claims=%7B%22userinfo%22%3A%20%7B%22email_verified%22%3A%20%7B%22reason%22%3A%20%22To%20know%20if%20your%20E-mail%20was%20verified%22%7D%2C%20%22email%22%3A%20%7B%22reason%22%3A%20%22To%20be%20able%20to%20contact%20you%22%2C%20%22essential%22%3A%20true%7D%2C%20%22name%22%3A%20%7B%22reason%22%3A%20%22To%20call%20you%20by%20name%22%7D%7D%7D
Please open the link:
https://auth.freedom-id.de/login?scope=openid&response_type=code&client_id=hmkzay2riyon4&redirect_uri=https%3A//foo.com/validate&login_hint=id200.connect.domains&state=&claims=%7B%22userinfo%22%3A%20%7B%22email_verified%22%3A%20%7B%22reason%22%3A%20%22To%20know%20if%20your%20E-mail%20was%20verified%22%7D%2C%20%22email%22%3A%20%7B%22reason%22%3A%20%22To%20be%20able%20to%20contact%20you%22%2C%20%22essential%22%3A%20true%7D%2C%20%22name%22%3A%20%7B%22reason%22%3A%20%22To%20call%20you%20by%20name%22%7D%7D%7D
Please enter code: >? 9jNXCX9OZ4HQLr2YZWKisw.5mSDkoR-5YJQoTp3f1vuxg
User Info:
{
    "aud": "hmkzay2riyon4", 
    "email": "foo@bar.de", 
    "email_verified": true, 
    "exp": 1538762218, 
    "iat": 1538761918, 
    "id4me.identifier": "id200.connect.domains", 
    "id4me.identity": "id200.connect.domains", 
    "iss": "https://auth.freedom-id.de", 
    "nbf": 1538761918, 
    "sub": "uiw3pTRRLVaKJqbnbSwr4EVuhEPTHvRgci91RbhYU2rab/YVDqDmqTKzTVAdDMm+", 
    "updated_at": 1538564738
}
```

### Requesting custom claims

In order to request a custom claim, it's enough to pass its name as a key in `userinfo_claims` or `id_token_claims`
parameters of `ID4meClient.get_consent_url` method.

Example
```python
...
        link = client.get_consent_url(
            ctx=context, 
            claimsrequest=ID4meClaimsRequest(
                userinfo_claims={
                    OIDCClaim.email: ID4meClaimRequestProperties(essential=True, reason='Test other confusing reason'),
                    'id4me.custom': ID4meClaimRequestProperties(essential=True, reason='Custom claim reason')
                })
        )
...
```

## CHANGELOG:
| version | date       | changes |
| ------- | -----------| ------ |
| 0.0.20  | 2019-05-23 | NEW FEATURE: E-mail address hashing as per spec change proposed in https://gitlab.com/ID4me/documentation/merge_requests/7<br>MINOR CHANGE: finally deprecated `preferred_client_id` from registration<br>NEW FEATURE: timeout configurable via NetworkConfig |
| 0.0.19  | 2019-03-24 | TEST: added Kopano to the integration test<br>BUGFIX: leeway to re-register set to 5 minutes istead of 2 hours<br>TEST: added password to mojeid test account |
| 0.0.18  | 2019-03-23 | NEW FEATURE: added support for E-mail like identifiers (just replace @ with .)<br>NEW FEATURE: requesting claims with scope<br>WORKAROUND: accepting token_type as 'Bearer' and 'bearer'<br>BUGFIX: 'tos_uri' assigned properly |
| 0.0.17  | 2019-03-19 | SECURITY FIX: Limited timeouts and size of downloaded data (DOS prevention)<br>SECURITY FIX: Limited recoursion level of distributed claims (DOS prevention) |
| 0.0.16  | 2019-03-11 | MAJOR CHANGE: removed back-compatibility with old _openid record format |
| 0.0.15  | 2019-02-27 | - NEW FEATURE: Automatically re-register expired client registration <br> - explicit parameter to enable/block automatic client registration |
| 0.0.14  | 2019-02-25 | No functional changes. Example code in README fixed |
| 0.0.13  | 2019-02-25 | No functional changes. TEST & EXAMPLE for custom claims added |
| 0.0.12  | 2019-02-21 | BUGFIX: Exception when no encryption used but private key missing |
| 0.0.11  | 2019-02-21 | BUGFIX, error when serializing ID4meContext |
| 0.0.10  | 2019-02-18 | API BREAKING CHANGE: client configuration loading callback moved to client object in order to remove secret data from the ID4meContext which can be in some frameworks sent over cookies |
