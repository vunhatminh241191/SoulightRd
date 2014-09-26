from allauth.account.models import EmailAddress

from soulightrd.apps.app_helper import get_user_login_object, generate_message, capitalize_first_letter

from soulightrd.settings import SITE_NAME

def activate_email_reminder_message(request,user_login):
	if "action" not in request.GET or "result" not in request.GET:	
		if user_login:
			email_confirmation = EmailAddress.objects.filter(email=user_login.email)
			if len(email_confirmation) != 0:
				if email_confirmation[0].verified == False: 
					data = {'user_login':user_login,'site_name': capitalize_first_letter(SITE_NAME)}
					return generate_message("confirm_email","asking",data)
		return None
