from django.db.models import Q

from cities_light.models import City

from soulightrd.apps.search.helper import build_city_autocomplete_data

import logging

logger = logging.getLogger(__name__)

city_autocomplete_data = build_city_autocomplete_data(City.objects.filter(Q(country__code2="US")|Q(country__code2="VN")),[])	

