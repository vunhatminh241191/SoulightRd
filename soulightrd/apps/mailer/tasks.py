from __future__ import absolute_import

from celery import shared_task

from soulightrd.apps.main.models import EmailTracking

from soulightrd.apps.mailer.helper import send_mass_email as send_mass_email_helper

import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email(email_tracking_id):
	try:
		email_tracking = EmailTracking.objects.get(id=email_tracking_id)
		email_tracking.send_email()
		logger.debug("Send email successfully")
	except Exception as e:
		logger.exception(e)


@shared_task
def send_mass_email(list_email_tracking_ids):
	try:
		send_mass_email_helper(list_email_tracking_ids)
		logger.debug("Send email successfully")
	except Exception as e:
		logger.exception(e)