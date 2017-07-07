from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import Template

from email_retargeting.models import Email
from email_retargeting.utils import send_email

@login_required
def resend(request, email_id):
	if request.user.is_superuser:

		e = Email.objects.get(id=email_id)

		subject = e.campaign.template.subject
		template = Template(e.campaign.template.body)

		e.failure = None

		send_email(e, subject, template, e.campaign.name)

		if e.failure is not None:
			messages.error(request, "There was a problem while sending the email.")
		else:
			messages.success(request, "Email has been send to %s" % e.to_email)

	return redirect('/admin/email_retargeting/email/')


