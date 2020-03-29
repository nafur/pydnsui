from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Zone(models.Model):
	name = models.CharField(
		max_length = 255,
		unique = True,
	)
	enabled = models.BooleanField(
		default = True,
		verbose_name = "Zone is enabled",
	)
	admins = models.ManyToManyField(User,
		verbose_name = "Admin users",
		help_text = "Users that may modify this zones records.",
	)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('zone-detail', kwargs = {
			'pk': self.pk,
		})


class Record(models.Model):
	class Meta:
		ordering = ["rname"]

	zone = models.ForeignKey(Zone,
		on_delete = models.CASCADE,
		verbose_name = "Zone",
		related_name = "records",
		editable = False,
	)
	rname = models.CharField(
		max_length = 255,
		verbose_name = "Record name",
	)
	rttl = models.IntegerField(
		verbose_name = "TTL",
	)
	rclass = models.CharField(max_length = 2,
		choices = [("IN", "IN"), ("CH", "CH"), ("HS", "HS"), ("CS", "CS")],
		default = "IN",
		verbose_name = "Record class",
	)
	rtype = models.CharField(
		max_length = 16,
		verbose_name = "Record type",
	)
	rdata = models.TextField(
		verbose_name = "Record data",
	)

	def __str__(self):
		return self.rname
	def get_absolute_url(self):
		return reverse('zone-detail', kwargs = {
			'pk': self.zone.pk
		})
