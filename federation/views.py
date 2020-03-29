from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.views.generic import base, edit

from pydnsui.views import *
from . import models

class RemoteManualImportView(FormHelperMixin, base.TemplateResponseMixin, edit.FormMixin, edit.ProcessFormView):
	form_class = forms.Form
	template_name = 'federation/remote_form.html'
	success_url = reverse_lazy('fed:remote-list')

	def download_from_remote(self, remote):
		print(remote)
		return {}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		remote = models.Remote.objects.get(pk = self.kwargs['pk'])
		context['data'] = self.download_from_remote(remote)
		return context

	def post(self, request, *args, **kwargs):
		print("Now we save all this")
		return super(RemoteManualImportView, self).post(request, *args, **kwargs)
