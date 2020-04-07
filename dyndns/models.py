from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

import config

class Zone(models.Model):
	zone = models.ForeignKey(
		config.models.Zone,
		on_delete = models.CASCADE,
		verbose_name = "Zone configuration",
		related_name = "zone_dyndns",
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "DynDNS for this zone is enabled.",
	)

	def __str__(self):
		return self.zone.name
	def get_absolute_url(self):
		return reverse('ddns:zone-detail', kwargs = {
			'pk': self.pk,
		})

class Host(models.Model):
	zone = models.ForeignKey(
		Zone,
		on_delete = models.CASCADE,
		verbose_name = "Zone",
		related_name = "hosts",
	)
	name = models.CharField(
		max_length = 255,
		help_text = "Hostname",
	)
	token = models.CharField(
		max_length = 255,
		help_text = "Authorization token for updating this host",
		default = get_random_string(length = 32),
	)
	last_update = models.DateTimeField(
		blank = True,
		null = True,
		editable = False,
		verbose_name = "Last update",
		help_text = "Last successful update."
	)

	def __str__(self):
		return self.zone.zone.name
	def get_absolute_url(self):
		return reverse('ddns:zone-detail', kwargs = {
			'pk': self.zone.pk,
		})
	def generate_new_token(self):
		self.token = get_random_string(length = 32)
