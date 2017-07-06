

class CampaignDoesNotExist(Exception):

	def __init__(self, campaign_name):
		self.campaign_name = campaign_name

	def __str__(self):
		return "Campaign '%s' does not exist" % self.campaign_name

