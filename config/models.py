from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Zone(models.Model):
	name = models.CharField(
		max_length = 255,
		unique = True,
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
