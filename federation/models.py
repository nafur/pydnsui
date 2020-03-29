from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from datetime import datetime

class Server(models.Model):
	name = models.CharField(
		max_length = 255,
		unique = True,
		help_text = "Unique identifier for this server. Maybe the FQDN?",
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "Zone is enabled",
	)
	admins = models.ManyToManyField(User,
		verbose_name = "Admin users",
		help_text = "Users that may modify this server.",
	)
	pull_url = models.URLField(
		blank = True,
		help_text = "URL where to pull the information.",
	)
	pull_enabled = models.BooleanField(
		default = True,
		verbose_name = "Pull is enabled",
	)
	pull_token = models.CharField(
		blank = True,
		max_length = 255,
		verbose_name = "Token",
	)
	pull_servers = models.ManyToManyField(
		'self',
		blank = True,
		verbose_name = "servers to pull from here",
		related_name = "servers",
	)
	pull_last = models.DateTimeField(
		blank = True,
		null = True,
		help_text = "Last pull from this server"
	)
	ipv4 = models.GenericIPAddressField(
		protocol = 'IPv4',
		verbose_name = "IPv4 address",
	)
	ipv6 = models.GenericIPAddressField(
		protocol = 'IPv6',
		verbose_name = "IPv6 address",
	)
	nameserver = models.CharField(
		max_length = 255,
		help_text = "FQDN of the nameserver",
	)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('fed:server-detail', kwargs = {
			'pk': self.pk,
		})
	def is_this_server(self):
		return settings.SERVER_NAME == self.name
	def is_push_recent(self):
		if self.last_push is None:
			return False
		return self.last_push > datetime.now() - datetime.hour(1)
	def is_receive_recent(self):
		if self.last_received is None:
			return False
		return self.last_received > datetime.now() - datetime.hour(1)

class Zone(models.Model):
	name = models.CharField(
		max_length = 255,
		unique = True,
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "Zone is enabled",
	)
	master = models.ForeignKey(Server,
		on_delete = models.CASCADE,
		verbose_name = "Master server",
		related_name = "zones_master",
	)
	slaves_all = models.BooleanField(
		default = True,
		verbose_name = "All servers are slaves",
	)
	slaves = models.ManyToManyField(Server,
		blank = True,
		verbose_name = "Slave servers",
		related_name = "zones_slave",
	)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('fed:zone-detail', kwargs = {
			'pk': self.pk,
		})
