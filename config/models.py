from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from pydnsui.models import *

class Zone(OwnedModel):
	name = models.CharField(
		max_length = 255,
		unique = True,
	)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('config:zone-detail', kwargs = {
			'pk': self.pk,
		})
