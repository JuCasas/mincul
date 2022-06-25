from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
	try:

		if(str(group_name) == 'Usuario Interno' and str((user.groups.get())) is not None):
			return True

		if (str((user.groups.get())) == str(group_name)):
			return True
		else:
			return False
	except:
		print("Usuario no loggeado")
		return False


