from django import forms

from . import models

class HostCreateForm(forms.ModelForm):
	class Meta:
		model = models.Host
		fields = ['zone', 'name']

	def __init__(self, *args, **kwargs):
		self.zone = kwargs.pop('zone')
		super(HostCreateForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance and instance.id:
			self.fields['zone'].widget.attrs['readonly'] = True

	def get_initial_for_field(self, field, field_name):
		if field_name == 'zone':
			return self.zone
