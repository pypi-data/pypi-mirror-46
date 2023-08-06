from django.conf import settings

from dj_authentication._util import import_object
from dj_authentication.openid import errors, verify


class IDUser(dict):
	is_authenticated = True


try:
	MAP_ID_TO_USER_FUNCTION = settings.MAP_ID_TO_USER_FUNCTION
except AttributeError:
	map_id_to_user = IDUser
else:
	map_id_to_user = import_object(MAP_ID_TO_USER_FUNCTION, 'map_id_to_user')


def get_user(request):
	params = dict(realm = settings.BASE_URL)

	token = request.http_auth('Bearer', params)
	if token is not None:
		try:
			id = verify(token)
		except errors.BadRequest:
			return
		except errors.Forbidden:
			return
		except errors.NotImplemented:
			return

		return map_id_to_user(id)
