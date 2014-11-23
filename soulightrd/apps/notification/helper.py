from django.template.loader import render_to_string

from soulightrd.apps.main.models import Notification

from soulightrd.apps.main.constants import NEW

from soulightrd.apps.app_settings import NOTIFICATION_SNIPPET_TEMPLATE
from soulightrd.apps.app_helper import get_user_login_object, generate_unique_id

def generate_notification_helper(notification_data,template,context_data):
	notify_users = notification_data['notify_users']
	notify_from = notification_data['notify_from']
	notification_type = notification_data['notification_type']
	if len(notify_users) > 0:
		notification_content = render_to_string(NOTIFICATION_SNIPPET_TEMPLATE[template],context_data)
		notification = Notification.objects.create(unique_id=generate_unique_id("notification"),
					content=notification_content,notification_type=notification_type,notify_from=notify_from)
		if notify_from in notify_users:
			notify_users.remove(notify_from)
		notification.notify_to.add(*notify_users)
		notification.save()


def get_new_notifications_count(request):
	user_login = get_user_login_object(request)
	return Notification.objects.filter(notify_to=user_login,status=NEW).count()
