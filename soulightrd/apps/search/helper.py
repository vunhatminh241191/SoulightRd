from soulightrd.settings import STATIC_URL
from soulightrd.apps.app_settings import LOGO_ICON_URL

import logging

logger = logging.getLogger(__name__)

def build_project_autocomplete_data(projects,container):
	return container

def build_organization_autocomplete_data(organizations,container):
	return container

def build_user_autocomplete_data(users,container):
	for user in users:
		try:
			data = {
				"value": user.username,
				"label": user.get_profile().get_user_fullname(),
				"type": "People",
				"url": "/people/" + user.username
			}
			if user.get_profile().avatar != None:
				data['picture'] = user.get_profile().avatar.image.url
			else:
				data['picture'] = LOGO_ICON_URL
			container.append(data)
		except Exception as e:
			logger.exception(e)
	return container