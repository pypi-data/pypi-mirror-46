from django.contrib.auth import get_user_model

User = get_user_model()


def map_email(id):
	user, created = User._default_manager.get_or_create(email = id['email'])
	user.backend = 'django.contrib.auth.backends.ModelBackend'
	return user


def map_sub_to_username(id):
	user, created = User._default_manager.get_or_create(username = id['sub'])
	user.backend = 'django.contrib.auth.backends.ModelBackend'
	return user
