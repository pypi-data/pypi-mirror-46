import os
from base64 import urlsafe_b64encode
from importlib import import_module

from openid_connect import errors, op, rp

from dj12 import _get_many
from django.conf import settings

from dj_authentication._util import import_object

try:
	PROVIDER = settings.OPENID_PROVIDER
except AttributeError:
	PROVIDER = None


def SimpleDjangoProvider(url):
	return op.Provider(
		url, key = dict(
			kty = 'oct',
			k = urlsafe_b64encode(settings.SECRET_KEY.encode('utf-8')).decode('utf-8'),
		))


def get_provider():
	if not PROVIDER:
		return None

	return import_object(PROVIDER, 'Provider')(settings.BASE_URL)


def get_relying_party():
	relying_party = rp.RelyingParty()

	provider = get_provider()
	if provider:
		relying_party.add_provider(provider)

	PROVIDERS = _get_many('AUTH_URL', None, lambda x: x)

	for client in PROVIDERS.values():
		if client:
			relying_party.add_provider(client)

	return relying_party


def issue(*args, **kwargs):
	return get_provider().issue(*args, **kwargs)


def verify(*args, **kwargs):
	return get_relying_party().verify(*args, **kwargs)
