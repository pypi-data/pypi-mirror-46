# Nice authentication support for Django

This is a simple, ready-to-use module for handling any standard kind of authentication in Django apps, without writing any code. However - if you have greater needs - this is also a uniform, configurable and extensible framework you can use to do whatever you need.

## Features
* Per-request authentication: common base for supporting any number of standard HTTP auth methods, and HTTP Basic and OAuth Bearer Token auth methods included
* OpenID Connect module: support for OpenID Connect token verification and issuance.
* Modular, uniform architecture: you can mix and match different auth mechanisms, and everything will just work!

We are only getting started. More generic auth mechanisms are going to be added in the future (see Planned features).

## Requirements
* Django 2.0+

## Installation
```sh
pip install dj-authentication
```

### settings.py
* Add `'dj_authentication'` to the list of `INSTALLED_APPS`.
* Remove `'django.contrib.auth.middleware.AuthenticationMiddleware'` from the list of `MIDDLEWARE`s.
* Add `dj_authentication.request_http_auth.HTTPAuthMiddleware` to the list of `MIDDLEWARE`s.
* Choose backends used for determining `request.user`, for example:
```python
REQUEST_USER_BACKENDS = [
    'dj_authentication.methods.basic', # HTTP Basic Auth
    'dj_authentication.methods.bearer', # OAuth Bearer Token Auth
    'django.contrib.auth',
]
```

## Per-request auth methods

### Basic auth
This method checks the provided username and password against configured Django authentication backends.

#### Tips
To trigger an authentication dialog in a browser, if the user is not authenticated:
```python
if not request.user.is_authenticated:
    return HttpResponse(status=401)
```

### Bearer auth
This method checks the provided bearer token against the OpenID Connect module, described below.

## `openid` module - OpenID Connect / OAuth support
`dj_authentication` includes an implementation of OpenID Connect / OAuth token verification and issuance.

You can configure the list of trusted OpenID Providers by providing their URLs thru `(*_)AUTH_URL` environment variables, like:
* `GOOGLE_AUTH_URL=https://client_id@accounts.google.com`
* `FACEBOOK_AUTH_URL=facebook+https://app_id@facebook.com`

All conforming OpenID Providers are supported; some other services too - see the list at [python-openid-connect](https://gitlab.com/aiakos/python-openid-connect). However, only conforming OpenID Providers that issue id_tokens are supported automatically in the Bearer auth.

### Token verification
You can verify tokens using:
* `dj_authentication.openid.verify()` function - on the OAuth callback URL, you should pass all the GET parameters you've received to this function. Some of the understood parameters are `id_token`, `iss` (for non-OpenID OAuth servers, for example `https://facebook.com`), `token_type`, `access_token`. Note that providing the `iss` parameter is **required** for legacy OAuth servers.
* `dj_authentication.methods.bearer` request.user backend - you can pass `id_token`s returned by the OpenID Providers in the `Authorization: Bearer` header, and this backend will automatically verify them to provide request.user.

#### How it works?
* For OpenID Providers, `id_token`s are verified against the [`jwks_uri`](https://tools.ietf.org/html/rfc8414#section-2).
* For supported legacy OAuth servers, `access_token`s are used to access userinfo endpoints and obtain user information.

#### User mapping
By default, `dj_authentication.methods.bearer` sets the `request.user` to a dict with the data decoded from the id_token, with `is_authenticated = True` property added.

To have it automatically map the ID data to a true user object, set the `MAP_ID_TO_USER_FUNC` variable. dj_authentication provides two ready-to-use functions:
* `'dj_authentication.user_mappings:map_email'` - it looks up the users by the email address
* `'dj_authentication.user_mappings:map_sub_to_username'` - it looks up the users using OpenID token subject as the username

### Issuing your own tokens
You can also issue and verify your own JWT id_tokens - just set `OPENID_PROVIDER = 'dj_authentication.openid:SimpleDjangoProvider'` in the `settings.py` file and use the `dj_authentication.openid.issue()` function. They will be signed with the Django `SECRET_KEY`.

## Example configurations

### App that supports session-less HTTP Basic auth in addition to standard Django sessions
```
REQUEST_USER_BACKENDS = [
    'dj_authentication.methods.basic',
    'django.contrib.auth',
]
```

### Session-less app that supports only Google id_tokens passed as Bearer tokens
```
AUTHENTICATION_BACKENDS = [] # Fully disable session-based auth; you may choose to delete django.contrib.auth from INSTALLED_APPS too.

REQUEST_USER_BACKENDS = [
    'dj_authentication.methods.bearer',
]

os.environ['GOOGLE_AUTH_URL'] = 'https://client_id@accounts.google.com'
```

### App that supports both email-based, Google and Facebook login
```
REQUEST_USER_BACKENDS = [
    'django.contrib.auth',
]

OPENID_PROVIDER = 'dj_authentication.openid:SimpleDjangoProvider' # for tokens sent in email verification messages

os.environ['GOOGLE_AUTH_URL'] = 'https://client_id@accounts.google.com'
os.environ['FACEBOOK_AUTH_URL'] = 'facebook+https://app_id@facebook.com'
```

### App that supports both email-based, Google and Facebook login; and session-less Google id_tokens passed as Bearer tokens
```
REQUEST_USER_BACKENDS = [
    'dj_authentication.methods.bearer',
    'django.contrib.auth',
]

OPENID_PROVIDER = 'dj_authentication.openid:SimpleDjangoProvider' # for tokens sent in email verification messages

MAP_ID_TO_USER_FUNC = 'dj_authentication.user_mappings:map_email'

os.environ['GOOGLE_AUTH_URL'] = 'https://client_id@accounts.google.com'
os.environ['FACEBOOK_AUTH_URL'] = 'facebook+https://app_id@facebook.com'
```

## Planned features
* Verification of `access_token` and `code` against `at_hash` and `c_hash` - to return them from `verify()`
* Support for opaque `id_token`s verified against a single configured OAuth/OIDC auth server thru [Introspection Endpoint](https://tools.ietf.org/html/rfc7662)
* Support for opaque `id_token`s verified against the Django session system (aka sending the session key as the Bearer token)
* Support for client certificates (see also [OAuth 2.0 Mutual TLS](https://tools.ietf.org/html/draft-ietf-oauth-mtls-12))
* Support for [OIDC `private_key_jwt` scheme](https://openid.net/specs/openid-connect-core-1_0.html#ClientAuthentication)
* Support for asymmetric signing methods for the issued tokens
