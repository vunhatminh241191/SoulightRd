import os, sys, string

SETTING_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_PATH = os.path.abspath(__file__ + "/../../../")

sys.path.append(SETTING_PATH)
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from soulightrd.apps.main.models import Organization

organization_names = list(string.ascii_uppercase)
string_integer = '1234567890'

def generate_phone(word, length):
	if len(word) == 1:
		return [word]
	current_perms = generate_phone(word[1:], length)
	perms = []
	[perms.append(x) for x in current_perms if x not in perms]
	char = word[0]
	result = []
	current_result = []
	for perm in perms:
		for i in range(len(perm) + 1):
			current_result.append(perm[:i] + char + perm[i:])
	for x in current_result:
		if x not in result and len(result) < length:
			result.append(x)
		elif x in result and len(result) < length:
			continue
		else:
			return result
	return result

def main():
	print "... RUNNING GENERATE ORGANIZATION SCRIPT ..."

	i = 0
	try:
		generated_phone = generate_phone(string_integer, len(organization_names))
		while i in range(len(organization_names)):
			organization = Organization.objects.create(unique_id=organization_names[i]
				, phone='+' + generated_phone[i], email= organization_names[i] + '@gmail.com')
			organization.save()
			i += 1
		print "Generate Organization successfully"
	except:
		print "Generate Organization Failed"
		raise

if __name__ == '__main__':
	stage = sys.argv[1]
	if stage != "prod":
		main()