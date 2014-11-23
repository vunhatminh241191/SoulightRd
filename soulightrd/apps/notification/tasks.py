from celery import shared_task

from soulightrd.apps.notification.helper import generate_notification_helper

@shared_task
def send_notification(notification_data,template,context_data):
	generate_notification_helper(notification_data,template,context_data)
