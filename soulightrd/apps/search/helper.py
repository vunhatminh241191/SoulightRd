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


def build_city_autocomplete_data(cities,container):
	for city in cities:
		try:
			data = {
				"value": city.name,
				"label": city.display_name,
				"picture": STATIC_URL + "img/apps/body/city_icon.jpg",
				"type": "City",
			}
			container.append(data)
		except Exception as e:
			logger.exception(e)
	return container