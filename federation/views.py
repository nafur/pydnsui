from django import forms
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.views.generic import base, detail, edit

from pydnsui.views import *
from . import models, pulling

from datetime import datetime
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
		- have one of the given subordinates
		"""
		try:
			print("Looking for remote {} with token {}".format(request.POST['remote'], request.POST['token']))
			remote = models.Remote.objects.get(auth_token = request.POST['token'])
			subordinates = request.POST.getlist('subordinates')
		except Exception as e:
			print(e)
			return HttpResponse('Invalid token', status = 401)
		print("Exporting zones for pulling server {} and subordinates {}".format(remote.name, subordinates))
		zones = models.Zone.objects.filter(
			Q(enabled = True) &
			Q(main__remote = None) & (
				Q(subordinates_all = True) | Q(subordinates__name__in = subordinates)
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
				"main": z.main.name,
				"subordinates_all": z.subordinates_all,
				"subordinates": list(map(lambda s: s.name, z.subordinates.all())),
			})
			servers.add(z.main)
			for s in z.subordinates.all():
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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			zones, p = pulling.get_zones(self.get_object())
			context['modified'] = p.modifications()
			context['warnings'] = p.warnings()
			context['server'] = self.get_object()
			context['zones'] = zones
		except urllib.request.HTTPError as e:
			context['error'] = e
		return context
	
	def post(self, request, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		pulling.pull_and_store(self.get_object())
		return super(PullManualView, self).post(request, *args, **kwargs)
