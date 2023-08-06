from importlib import import_module

from django.conf import settings

if 'django.contrib.auth' in settings.INSTALLED_APPS:
	from django.contrib.auth.models import AnonymousUser
else:

	class AnonymousUser:
		is_authenticated = False
		pass


class Anon(AnonymousUser):
	def __bool__(self):
		return False


try:
	backend_names = settings.REQUEST_USER_BACKENDS
except AttributeError:
	backend_names = [
		'django.contrib.auth',
	]


def import_object(path, def_name):
	try:
		mod, cls = path.split(':', 1)
	except ValueError:
		mod = path
		cls = def_name

	return getattr(import_module(mod), cls)


backends = [import_object(path, 'get_user') for path in backend_names]


def get_request_user(request):
	try:
		return request._user
	except AttributeError:
		for get_user in backends:
			user = get_user(request)
			if user and user.is_authenticated:
				request._user = user
				break
		else:
			request._user = Anon()

	return request._user


def set_request_user(request, user):
	if user.is_authenticated:
		request._user = user
	else:
		request._user = Anon()


request_user = property(get_request_user, set_request_user)


def drf_get_request_user(request):
	return request._request.user


def drf_set_request_user(request, user):
	request._request.user = user


drf_request_user = property(drf_get_request_user, drf_set_request_user)
