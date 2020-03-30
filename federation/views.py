from django import forms
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.views.generic import base, detail, edit

from pydnsui.views import *
from . import models

import json
import urllib.parse
import urllib.request

@method_decorator(csrf_exempt, name='dispatch')
class ExportZonesView(View):
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		try:
			server = models.Server.objects.get(auth_token = request.POST['token'])
		except:
			return HttpResponse('Invalid token', status = 401)
		zones = models.Zone.objects.filter(
			~Q(master = server) & Q(enabled = True) & (Q(slaves_all = True) | Q(slaves = server))
		)
		res = []
		for z in zones:
			res.append({
				"name": z.name,
				"master": z.master.name,
				"slaves_all": z.slaves_all,
				"slaves": list(map(lambda s: s.name, z.slaves.all())),
			})
		return JsonResponse(res, safe = False)

class PullManualView(detail.SingleObjectMixin, FormHelperMixin, base.TemplateResponseMixin, edit.FormMixin, edit.ProcessFormView):
	form_class = forms.Form
	model = models.Server
	object = None
	template_name = 'federation/pull_form.html'
	success_url = reverse_lazy('fed:server-list')

	def download_from_server(self):
		server = self.get_object()
		data = urllib.parse.urlencode({"token": server.pull_token}).encode("utf8")
		u = urllib.request.urlopen(server.pull_url, data = data)
		return json.loads(u.read().decode('utf8'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['data'] = self.download_from_server()
		except urllib.request.HTTPError as e:
			context['error'] = e
		return context
	
	def get_or_create_server(self, name):
		try:
			return models.Server.objects.get(name = name)
		except:
			s = models.Server(name = name)
			s.save()
			return s

	def post(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		zones = self.download_from_server()
		print(zones)
		for zone in zones:
			master = self.get_or_create_server(zone['master'])
			z = models.Zone.objects.filter(master = master, name = zone['name'])
			if not z:
				print("New zone")
				z = models.Zone(master = master, name = zone['name'])
			else:
				print(z)
				z = z[0]
			z.enabled = True
			z.slaves_all = zone['slaves_all']
			z.save()
			z.slaves.set(map(lambda s: self.get_or_create_server(s), zone['slaves']))
		return super(PullManualView, self).post(request, *args, **kwargs)
