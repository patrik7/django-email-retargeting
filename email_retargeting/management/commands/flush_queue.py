# -*- coding: utf-8
import sys
from django.core.management.base import BaseCommand
from django.template import Template
from django.utils import timezone

from email_retargeting.models import Campaign
from email_retargeting.utils import send_email

from django.db import transaction

import logging
from rollbar import report_exc_info

logger = logging.getLogger('emailing')

class CampaignLockGuard():

	def __init__(self, campaign_id):
		self.campaign_id = campaign_id

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_val, exc_tb):
		c = Campaign.objects.get(id=self.campaign_id)
		c.processing = False
		c.save()



class Command(BaseCommand):
	help = 'Send emails scheduled for sending'

	def handle(self, *args, **options):
		for c in Campaign.objects.filter(live=True):

			try:
				count = c.email_set.filter(sent_at=None).count()

				if count > 0:

					with transaction.atomic():
						#fetch again
						campaing = Campaign.objects.get(id=c.id)

						if not campaing.processing:
							campaing.processing = True
							campaing.save()

						else:
							continue

					#Send emails
					with CampaignLockGuard(c.id):
						logger.info("Processing emails(%d) from campaign %s" % (count, c.name))

						emails = campaing.email_set.filter(sent_at=None)

						template = Template(campaing.template.body)
						subject = campaing.template.subject

						for e in emails:
							if e.send_after is not None and e.send_after > timezone.now():
								continue

							send_email(e, subject, template, c.name)

			except:
				report_exc_info()