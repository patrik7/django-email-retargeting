from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django.db import models
import importlib


class EmailTemplate(models.Model):

	name = models.CharField(_("Template name"),max_length=128,unique=True,null=False)

	subject = models.CharField(max_length=256,null=False)
	body = models.TextField(_("Email body"), max_length=80000,null=False)

	def __unicode__(self):
		return self.name


class Campaign(models.Model):
	name = models.CharField(max_length=128,null=False,unique=True)

	from_email = models.CharField(max_length=256,blank=True,default='')

	template = models.ForeignKey(EmailTemplate,null=False)

	live = models.BooleanField(default=False,null=False)

	processing = models.BooleanField(default=False,null=False)

	def __unicode__(self):
		return "%s (%s)" % (self.name, "on hold" if not self.live else "live")


class Email(models.Model):
	campaign = models.ForeignKey(Campaign,null=False)
	from_email = models.CharField(max_length=256,blank=True,default='')
	to_email = models.EmailField(null=False)

	domain = models.CharField(max_length=128,null=False,default='bovine.ch')

	sent_at = models.DateTimeField(null=True,default=None,blank=True)
	failure = models.CharField(max_length=512,blank=True,default='')

	dictionary = models.TextField(null=False,default="{}",max_length=4096)

	send_after = models.DateTimeField(null=True,blank=True)
	send_condition = models.CharField(max_length=256,blank=True,default='')

	def send_explain(self):
		if self.send_after is None:
			return 'Right away'
		else:
			if self.send_condition is not None:
				return 'Conditionally after %s' % self.send_after
			else:
				return 'After %s' % self.send_after

	def evaluate_condition(self):
		if self.send_condition is None:
			return True

		module_name = self.send_condition.split('.')[0]

		module = importlib.import_module(module_name)

		return eval(self.send_condition, {module_name: module})
