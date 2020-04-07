from django.shortcuts import render
from django.urls import reverse_lazy

from pydnsui.views import *

from . import forms, models

class HostCreateView(CrispyCreateView):
	model = models.Host
	form_class = forms.HostCreateForm
	template_name = 'dyndns/host_form.html'
	form_submit_text = 'Submit'

	def get_form_kwargs(self):
		kwargs = super(HostCreateView, self).get_form_kwargs()
		kwargs['zone'] = models.Zone.objects.get(pk = self.kwargs['pk'])
		return kwargs

class HostDeleteView(CrispyDeleteView):
	model = models.Host
	
	def get_success_url(self):
		return reverse_lazy('ddns:zone-detail', kwargs = {
			'pk': self.get_object().zone.pk
		})

class HostRenewTokenView(CrispyUpdateView):
	model = models.Host
	template_name = 'dyndns/host_renew_token_form.html'
	fields = []
	
	def get_success_url(self):
		return reverse_lazy('ddns:zone-detail', kwargs = {
			'pk': self.get_object().zone.pk
		})
	
	def post(self, request, *args, **kwargs):
		obj = self.get_object()
		print(type(obj.token))
		obj.generate_new_token()
		obj.save()
		return super(HostRenewTokenView, self).post(request, *args, **kwargs)
