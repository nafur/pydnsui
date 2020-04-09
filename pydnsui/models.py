from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.core.exceptions import PermissionDenied

from cuser.middleware import CuserMiddleware

class OwnedModel(models.Model):
	class Meta:
		abstract = True

	owners = models.ManyToManyField(User,
		verbose_name = "Owners",
		related_name = "+", #"set_{}_{}".format(__module__.replace('.', '_'), __name__), 
		help_text = "Users that are allowed to modify this object. Staff users can modify all objects.",
	)

	def is_owned(self):
		user = CuserMiddleware.get_user()
		if user is None:
			return False
		if user.is_staff:
			return True
		return self.owners.filter(id = user.pk).exists()

	def save(self, *args, **kwargs):
		if self.pk is None:
			super().save(*args, **kwargs)
			self.owners.add(CuserMiddleware.get_user())
		elif self.is_owned():
			super().save(*args, **kwargs)
		else:
			raise PermissionDenied()

	def delete(self, *args, **kwargs):
		if self.is_owned():
			super().delete(*args, **kwargs)