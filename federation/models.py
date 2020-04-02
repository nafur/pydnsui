from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
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
	configured_here = models.BooleanField(
		default = True,
		verbose_name = "Zones for this server are configured here.",
	)
	admins = models.ManyToManyField(User,
		verbose_name = "Admin users",
		help_text = "Users that may modify this server.",
	)
	auth_token = models.CharField(
		max_length = 255,
		default = "",
		verbose_name = "Authorization token",
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
		symmetrical = False,
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
	@staticmethod
	def get_this_server():
		return Server.objects.get(name = settings.SERVER_NAME)
	@staticmethod
	def get_other_servers():
		return Server.objects.exclude(name = settings.SERVER_NAME)

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
	
	@staticmethod
	def get_master_zones():
		return Zone.objects.filter(
			Q(enabled = True) & Q(master = Server.get_this_server())
		)
	@staticmethod
	def get_slave_zones():
		this_server = Server.get_this_server()
		return Zone.objects.filter(
			Q(enabled = True) & (
				Q(slaves = this_server) |
				(Q(slaves_all = True) & ~Q(master = this_server))
			)
		)
