import json

data = json.loads(open('cities.json').read())

f = open("built_city_data.json","w")

LIST_COUNTRIES_ID = [242]
LIST_COUNTRIES_CODE = ["VN"]

s = "["
for item in data:
	model = item['model']
	if model == "cities_light.country":
		if item['fields']['code2'] in LIST_COUNTRIES_CODE:
			s = s + str(json.dumps(item,indent=2))
			s = s + ","
	if model == "cities_light.city" or model == "cities_light.region":
		if item['fields']['country'] in LIST_COUNTRIES_ID:
			s = s + str(json.dumps(item,indent=2))
			s = s + ","
s = s[:len(s)-1] + "]"
f.write(s)
f.close()
