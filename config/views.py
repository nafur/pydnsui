from django import forms
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import *
from django.views.generic import base, detail, edit

from pydnsui.views import *
from . import forms as models
import federation

import dns
import subprocess

from config.forms import *
from config import dnsutils

class ZoneDetailView(DetailView):
	model = models.Zone

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = dnsutils.get_zone_records(settings.BIND_SERVER_NAME, self.get_object().name)
		return context

class RecordCreateView(FormHelperMixin, base.TemplateResponseMixin, edit.FormMixin, edit.ProcessFormView):
	form_class = RecordForm
	form_submit_text = 'Submit'
	template_name = 'config/record_form.html'
	
	def get_success_url(self):
		return reverse_lazy('zone-detail', kwargs = {'pk': self.kwargs['zone']})

	def form_valid(self, form):
		if form.is_valid():
			zone = models.Zone.objects.get(pk = self.kwargs['zone'])
			u = dnsutils.Updater(settings.BIND_SERVER_NAME, zone.name)
			u.add(form.cleaned_data)
			u.send()
		return super(RecordCreateView, self).form_valid(form)

class RecordUpdateView(FormHelperMixin, base.TemplateResponseMixin, edit.FormMixin, edit.ProcessFormView):
	form_class = RecordForm
	form_submit_text = 'Submit'
	template_name = 'config/record_form.html'
	
	def get_success_url(self):
		print("Was called!")
		return reverse_lazy('zone-detail', kwargs = {'pk': self.kwargs['zone']})
	
	def get_initial(self):
		initial = super(RecordUpdateView, self).get_initial()
		initial.update(dnsutils.unserialize(self.kwargs['serialized']))
		return initial
	
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			zone = models.Zone.objects.get(pk = self.kwargs['zone'])
			u = dnsutils.Updater(settings.BIND_SERVER_NAME, zone.name)
			u.delete(dnsutils.unserialize(self.kwargs['serialized']))
			u.add(form.cleaned_data)
			response = u.send()
			if response.rcode() == dns.rcode.NOERROR:
				return self.form_valid(form)
		return self.render_to_response(self.get_context_data(form = form, error = response))

class RecordDeleteView(base.TemplateResponseMixin, edit.FormMixin, edit.ProcessFormView):
	form_class = forms.Form
	template_name = 'config/record_confirm_delete.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['record'] = dnsutils.unserialize(self.kwargs['serialized'])
		return context

	def post(self, request, *args, **kwargs):
		zone = models.Zone.objects.get(pk = self.kwargs['zone'])
		u = dnsutils.Updater(settings.BIND_SERVER_NAME, zone.name)
		u.delete(dnsutils.unserialize(self.kwargs['serialized']))
		u.send()
		return HttpResponseRedirect(reverse('zone-detail', kwargs = {'pk': self.kwargs['zone']}))

class ZoneDeployView(FormHelperMixin, base.TemplateResponseMixin, edit.FormMixin, edit.ProcessFormView):
	form_class = forms.Form
	template_name = 'config/deploy_form.html'
	success_url = reverse_lazy('zone-list')
	
	def render_configuration(self):
		files = []
		warnings = []
		for zone in models.Zone.objects.all():
			slaves = []
			try:
				fedzone = federation.models.Zone.objects.get(name = zone.name)
				slaves = fedzone.get_slaves()
			except:
				warnings.append("The zone {} is configured locally, but not configured in the federation.".format(zone.name))
			
			files.append({
				'name': zone.name,
				'filename': settings.BIND_CONFIG_DIR + '{}.conf'.format(zone.name),
				'content': render_to_string('config/bind_zone.tpl', {
					'basedir': settings.BIND_CONFIG_DIR,
					'zone': zone,
					'slaves': slaves,
				}),
				'include': True,
			})
			files.append({
				'name': 'db.{}'.format(zone.name),
				'filename': settings.BIND_CONFIG_DIR + 'db.{}'.format(zone.name),
				'content': render_to_string('config/bind_db.tpl', {
					'zone': zone,
				}),
				'include': False,
			})
		
		for zone in federation.models.Zone.get_slave_zones():
			files.append({
				'name': zone.name,
				'filename': settings.BIND_CONFIG_DIR + 'slave_{}.conf'.format(zone.name),
				'content': render_to_string('config/bind_slave_zone.tpl', {
					'basedir': settings.BIND_CONFIG_DIR,
					'zone': zone,
					'slaves': zone.get_slaves(),
				}),
				'include': True,
			})
		
		files.insert(0, {
			'name': 'main.conf',
			'active': True,
			'filename': settings.BIND_CONFIG_DIR + 'main.conf',
			'content': render_to_string('config/bind_main.tpl', {
				'zones': map(lambda z: z['filename'], filter(lambda f: f['include'], files)),
			})
		})
		return files, warnings

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['files'], context['warnings'] = self.render_configuration()
		return context
	
	def post(self, request, *args, **kwargs):
		print("Now we configure the server")
		errors = []
		files, _ = self.render_configuration()
		for file in files:
			print("Writing to {}".format(file['filename']))
			try:
				f = open(file['filename'], 'w')
				f.write(file['content'])
				f.close()
			except Exception as e:
				errors.append(e)
		try:
			res = subprocess.run(settings.BIND_RELOAD_CMD, shell = False, capture_output = True)
			if res.returncode != 0:
				errors.append("Runnning {} failed:\n\n{}".format(" ".join(settings.BIND_RELOAD_CMD), res.stderr.decode('utf8')))
		except Exception as e:
			errors.append(e)
		if errors is not []:
			return TemplateResponse(request, 'config/deploy_error.html', {'errors': errors})
		return super(DeployView, self).post(request, *args, **kwargs)
