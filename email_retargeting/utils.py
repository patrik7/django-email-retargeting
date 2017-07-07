import errno
import traceback

from django.conf import settings
from django.template.defaultfilters import urlencode
from django.utils import timezone

from email_retargeting.models import Campaign, Email
from email_retargeting.exceptions import CampaignDoesNotExist


from django.template import Template, Context
from django.core.mail import send_mail, EmailMultiAlternatives
from bs4 import BeautifulSoup

import json

import os
import codecs

from django.utils import translation

import logging
logger = logging.getLogger('emailing')

def schedule_send_email(campaign_name, to_email, domain, dictionary, from_email=None, now=False, send_after=None, send_condition=None):

	if settings.IS_TEST:
		return

	try:
		c = Campaign.objects.get(name=campaign_name)
	except Campaign.DoesNotExist:
		raise CampaignDoesNotExist(campaign_name)

	e = Email(campaign=c, to_email=to_email, from_email=from_email or c.from_email, domain=domain, dictionary=json.dumps(dictionary), send_after=send_after, send_condition=send_condition)
	e.save()

	if now and c.live:
		subject = c.template.subject
		template = Template(c.template.body)

		send_email(e, subject, template, campaign_name)

	return e


def send_email(e, subject_raw, template, campaign = 'email_retargeting'):

	try:
		if e.send_condition is not None:
			if not e.evaluate_condition():
				logger.info("Deleting email '%s', based on failing condition to send" % e)
				e.delete()
				return

		dictionary = json.loads(e.dictionary)

		dictionary['subject'] = subject_raw % dictionary
		dictionary['domain'] = e.domain

		dictionary['utms'] = 'utm_source=email&utm_medium=email&utm_nooverride=1&utm_campaign=%s' % urlencode(e.campaign.name)


		#add UTMs
		for k in filter(lambda k: k[:4] == 'url_', dictionary.keys()):
			if dictionary[k].find('?') == -1:
				dictionary[k] = dictionary[k] + "?" + dictionary['utms']

		translation.activate('cs_CZ')
		rendered_body = template.render(Context(dictionary))

		is_html = rendered_body[:400].lower().find('<html') != -1

		if is_html:
			html = rendered_body
			message = BeautifulSoup(html, "html.parser").text
		else:
			html = None
			message = rendered_body

		dir = settings.EMAIL_DUMP_DIRECTORY

		if dir:
			filename = os.path.join(dir, timezone.now().strftime("%y-%m-%d_%H%M%S_%f") + "_" + dictionary['subject'] + "." + ('.html' if is_html else '.txt'))

			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise

			f = codecs.open(filename, "w", "utf-8")
			f.write(html if is_html else message)
			f.close()

		else:
			if is_html:
				msg = EmailMultiAlternatives(dictionary['subject'], message, e.from_email, [e.to_email], headers={
					'X-Mailgun-Tag': campaign
				})
				msg.attach_alternative(html, "text/html")
				msg.send()

			else:

				send_mail(
					subject=dictionary['subject'],
					message=message,
					from_email=e.from_email,
					recipient_list=[e.to_email],
					fail_silently=False
				)

		e.sent_at = timezone.now()
		e.failure = None
		e.save()

	except Exception as ex:
		e.failure = ex.__str__();
		e.save()
