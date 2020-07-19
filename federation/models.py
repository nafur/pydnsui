from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils import timezone

from pydnsui.models import *

from datetime import datetime, timedelta

class Remote(OwnedModel):
	name = models.CharField(
		max_length = 255,
		unique = True,
		help_text = "Unique identifier for this remote. Maybe the FQDN?",
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "Remote is enabled",
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


class Server(OwnedModel):
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

class Zone(OwnedModel):
	name = models.CharField(
		max_length = 255,
		unique = True,
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "Zone is enabled",
	)
	main = models.ForeignKey(Server,
		on_delete = models.CASCADE,
		verbose_name = "Main server",
		related_name = "zones_main",
	)
	subordinates_all = models.BooleanField(
		default = True,
		verbose_name = "All servers are subordinates",
	)
	subordinates = models.ManyToManyField(Server,
		blank = True,
		verbose_name = "Subordinate servers",
		related_name = "zones_subordinate",
	)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('fed:zone-detail', kwargs = {
			'pk': self.pk,
		})
	
	def get_nameservers(self):
		return [self.main.nameserver] + [
			s.nameserver for s in self.get_subordinates()
		]
	
	def get_subordinates(self):
		if self.subordinates_all:
			return Server.objects.filter(
				Q(enabled = True) & ~Q(pk = self.main.pk)
			)
		return self.subordinates.all()

	@staticmethod
	def get_subordinate_zones():
		servers = Server.objects.filter(remote = None)
		return Zone.objects.filter(
			Q(enabled = True) & (
				Q(subordinates__in = servers) |
				(Q(subordinates_all = True) & ~Q(main__in = servers))
			)
		)
