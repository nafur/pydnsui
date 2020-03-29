from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Server(models.Model):
	name = models.CharField(
		max_length = 255,
		unique = True,
		help_text = "Unique identifier for this server. Maybe the FQDN?",
	)
	admins = models.ManyToManyField(User,
		verbose_name = "Admin users",
		help_text = "Users that may modify this server.",
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
	token = models.CharField(
		max_length = 255,
		verbose_name = "Token",
	)
	last_poll = models.DateTimeField(
		null = True,
		blank = True,
		verbose_name = "Last polled",
	)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('fed:server-detail', kwargs = {
			'pk': self.pk,
		})
	def is_this_server(self):
		return settings.SERVER_NAME == self.name

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
