from django.contrib import admin
from django.urls import reverse

from email_campaigns.models import Campaign, Email, EmailTemplate

class CampaignAdmin(admin.ModelAdmin):
	list_display = ['name', 'template', 'live']
	pass


class EmailTemplateAdmin(admin.ModelAdmin):
	list_display = ['name', 'subject']
	pass


class EmailAdmin(admin.ModelAdmin):
	list_display = ['to_email', 'campaign', 'send_explain', 'sent_at', 'failed', 'resend']
	search_fields = ['to_email']

	def failed(self, email):
		return 'Failed' if email.failure is not None else ''
	failed.short_description = 'Failed'

	def resend(self, email):
		return '<a href="%s">Resend</a>' % reverse("admin_email_resend", kwargs={'email_id': email.id})
	resend.short_description = 'Resend email'
	resend.allow_tags = True


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Email, EmailAdmin)
