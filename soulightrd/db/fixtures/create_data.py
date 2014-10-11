import json, os, sys

SETTING_PATH = os.path.abspath(__file__ + "/../../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../../")

sys.path.append(PROJECT_PATH)
sys.path.append(SETTING_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

data = json.loads(open('built_city_data.json').read())

from cities_light.models import City, Region, Country
from django.db.models import Q

Country.objects.all().delete()
Region.objects.all().delete()
City.objects.all().delete()

regions = []
cities = []
for item in data:
	try:
		model = item['model']
		if model == "cities_light.country":
			country = Country.objects.create(id=item['pk'],
										code2=item['fields']['code2'], 
										code3=item['fields']['code3'], 
										name=item['fields']['name'], 
										name_ascii=item['fields']['name_ascii'], 
										alternate_names=item['fields']['alternate_names'], 
										slug=item['fields']['slug'], 
										geoname_id=item['fields']['geoname_id'], 
										phone=item['fields']['phone'], 
										tld=item['fields']['tld'], 
										continent=item['fields']['continent'])

		if model == "cities_light.region":
			country = Country.objects.get(id=item['fields']['country'])
			region = Region.objects.create(
				id=item['pk'],
				display_name=item['fields']['display_name'], 
				name=item['fields']['name'], 
				country=country, 
				alternate_names=item['fields']['alternate_names'], 
				geoname_id=item['fields']['geoname_id'], 
				geoname_code=item['fields']['geoname_code'], 
				name_ascii=item['fields']['name_ascii'], 
				slug=item['fields']['slug']
			)
		if model == "cities_light.city":
			country = Country.objects.get(id=item['fields']['country'])
			region = Region.objects.get(id=item['fields']['region'])
			city = City(
						id=item['pk'],
						display_name=item['fields']['display_name'], 
						name=item['fields']['name'], 
						country=country, 
						region=region, 
						alternate_names=item['fields']['alternate_names'], 
						search_names=item['fields']['search_names'], 
						longitude=item['fields']['longitude'], 
						geoname_id=item['fields']['geoname_id'], 
						feature_code=item['fields']['feature_code'], 
						name_ascii=item['fields']['name_ascii'], 
						latitude=item['fields']['latitude'], 
						slug=item['fields']['slug'], 
						population=item['fields']['population']
					)
			cities.append(city)
	except Exception as e:
		print e
		pass

City.objects.bulk_create(cities)

			

