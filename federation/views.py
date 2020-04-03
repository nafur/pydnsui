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
		"""
		Use server and token for authorization.
		Export all zones that
		- are enabled
		- belong to a server configured locally
		- have one of the given slaves
		"""
		try:
			print("Looking for remote {} with token {}".format(request.POST['remote'], request.POST['token']))
			remote = models.Remote.objects.get(auth_token = request.POST['token'])
			slaves = request.POST.getlist('slaves')
		except Exception as e:
			print(e)
			return HttpResponse('Invalid token', status = 401)
		print("Exporting zones for pulling server {} and slaves {}".format(remote.name, slaves))
		zones = models.Zone.objects.filter(
			Q(enabled = True) &
			Q(master__remote = None) & (
				Q(slaves_all = True) | Q(slaves__name__in = slaves)
			)
		)
		res = {
			'zones': [],
			'server': {},
		}
		servers = set()
		for z in zones:
			res['zones'].append({
				"name": z.name,
				"master": z.master.name,
				"slaves_all": z.slaves_all,
				"slaves": list(map(lambda s: s.name, z.slaves.all())),
			})
			servers.add(z.master)
			for s in z.slaves.all():
				servers.add(s)
		for s in servers:
			res['server'][s.name] = {
				'ipv4': s.ipv4,
				'ipv6': s.ipv6,
				'nameserver': s.nameserver,
			}
		return JsonResponse(res, safe = False)

class PullManualView(detail.SingleObjectMixin, FormHelperMixin, base.TemplateResponseMixin, edit.FormMixin, edit.ProcessFormView):
	form_class = forms.Form
	model = models.Remote
	object = None
	template_name = 'federation/pull_form.html'
	success_url = reverse_lazy('fed:remote-list')

	def download_from_remote(self):
		remote = self.get_object()
		slaves = models.Server.objects.filter(remote = None, enabled = True)
		data = urllib.parse.urlencode({
			'remote': remote.name, 
			'token': remote.pull_token,
			'slaves': [s.name for s in slaves],
		}, True).encode("utf8")
		print("Queried {} with {}".format(remote.pull_url, data))
		u = urllib.request.urlopen(remote.pull_url, data = data)
		res = json.loads(u.read().decode('utf8'))
		print("Got {}".format(res))
		return res
	
	def postprocess_data(self, data):
		missing_server = []
		for s in data['server']:
			s = self.get_or_create_server(s)
			if not s.pk:
				s.ipv4 = data['server'][s.name]['ipv4']
				s.ipv6 = data['server'][s.name]['ipv6']
				s.nameserver = data['server'][s.name]['nameserver']
				s.remote = self.get_object()
				missing_server.append(s)
			data['server'][s.name] = s
		zones = []
		for zone in data['zones']:
			zone['master'] = data['server'][zone['master']]
			zone['slaves'] = list(map(lambda s: data['server'][s], zone['slaves']))
			zones.append(zone)
		return (zones, missing_server)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			data = self.download_from_remote()
			zones, missing = self.postprocess_data(data)
			context['missing'] = missing
			context['server'] = self.get_object()
			context['zones'] = zones
		except urllib.request.HTTPError as e:
			context['error'] = e
		return context
	
	def get_or_create_server(self, name, save = False):
		try:
			return models.Server.objects.get(name = name)
		except:
			s = models.Server(name = name)
			if save:
				s.save()
			return s

	def post(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		data = self.download_from_remote()
		zones, missing = self.postprocess_data(data)
		for m in missing:
			m.save()
		for zone in zones:
			try:
				z = models.Zone.objects.get(name = zone['name'])
			except models.Zone.DoesNotExist as e:
				z = models.Zone(
					name = zone['name'],
					master = zone['master'],
					slaves_all = zone['slaves_all']
				)
				z.save()
				z.slaves.set(zone['slaves'])
			continue
			z = models.Zone.objects.filter(master = zone['master'], name = zone['name'])
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
