from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils import timezone

from datetime import datetime, timedelta

class Remote(models.Model):
	name = models.CharField(
		max_length = 255,
		unique = True,
		help_text = "Unique identifier for this remote. Maybe the FQDN?",
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "Remote is enabled",
	)
	admins = models.ManyToManyField(User,
		verbose_name = "Admin users",
		help_text = "Local users that may modify this remote.",
	)
	auth_token = models.CharField(
		max_length = 255,
		blank = True,
		unique = True,
		verbose_name = "Authorization token",
		help_text = "The token this remote should use for pulling zone information.",
	)
	pull_url = models.URLField(
		blank = True,
		verbose_name = "Pull URL",
		help_text = "URL to pull zone information from this remote.",
	)
	pull_token = models.CharField(
		blank = True,
		max_length = 255,
		verbose_name = "Pull Token",
		help_text = "The token used for pulling zone information, should correspond to the authorization token on this remote.",
	)
	pull_last = models.DateTimeField(
		blank = True,
		null = True,
		verbose_name = "Last pull",
		help_text = "Last successful pull from this remote."
	)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('fed:remote-detail', kwargs = {
			'pk': self.pk,
		})
	def is_pull_recent(self):
		if self.pull_last is None:
			return False
		return self.pull_last > timezone.now() - timedelta(hours = 1)


class Server(models.Model):
	class Meta:
		ordering = [F('remote').asc(nulls_last = False), 'name']
	name = models.CharField(
		max_length = 255,
		unique = True,
		help_text = "Unique identifier for this server. Maybe the FQDN?",
	)
	remote = models.ForeignKey(
		Remote,
		null = True,
		on_delete = models.CASCADE,
		verbose_name = "Responsible remote",
		help_text = "Remote that introduced this server",
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "Server is enabled",
	)
	ipv4 = models.GenericIPAddressField(
		protocol = 'IPv4',
		verbose_name = "IPv4 address",
		help_text = "IPv4 address of the nameserver for the bind query settings.",
	)
	ipv6 = models.GenericIPAddressField(
		protocol = 'IPv6',
		verbose_name = "IPv6 address",
		help_text = "IPv6 address of the nameserver for the bind query settings.",
	)
	nameserver = models.CharField(
		max_length = 255,
		verbose_name = "Nameserver",
		help_text = "Proper FQDN of the nameserver for the NS entries.",
	)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('fed:server-detail', kwargs = {
			'pk': self.pk,
		})
	def is_this_server(self):
		return settings.SERVER_NAME == self.name
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
