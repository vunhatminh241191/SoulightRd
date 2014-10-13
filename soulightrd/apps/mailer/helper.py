from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings as django_settings

from soulightrd.apps.main.models import EmailTracking

import logging, datetime

logger = logging.getLogger(__name__)

def send_mass_email(list_email_tracking_id):
	emails = EmailTracking.objects.filter(id__in=list_email_tracking_id)
	list_send_emails = []
	for email in emails:
		list_send_emails.append(email.generate_email())
	try:
		connection = get_connection()
		connection.open()
		connection.send_messages(list_send_emails)
		connection.close()
		EmailTracking.objects.filter(id__in=list_email_tracking_id).update(status='success',send_time=datetime.datetime.now())
	except Exception as e:
		logger.exception(e)
		EmailTracking.objects.filter(id__in=list_email_tracking_id).update(status='fail')


