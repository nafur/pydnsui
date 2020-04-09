from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from pydnsui.views import *
from config import dnsutils

from . import forms, models

class HostCreateView(CrispyCreateView):
	model = models.DynHost
	form_class = forms.HostCreateForm
	template_name = 'dyndns/dynhost_form.html'
	form_submit_text = 'Submit'

	def get_form_kwargs(self):
		kwargs = super(HostCreateView, self).get_form_kwargs()
		kwargs['zone'] = models.DynZone.objects.get(pk = self.kwargs['pk'])
		return kwargs

class HostDeleteView(CrispyDeleteView):
	model = models.DynHost
	
	def get_success_url(self):
		return reverse_lazy('ddns:zone-detail', kwargs = {
			'pk': self.get_object().zone.pk
		})

class HostDetailView(DetailView):
	model = models.DynHost

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		BASE_URL = 'https://dns.gereon-kremer.de'
		context['endpoints'] = [
			{
				'active': True,
				'id': 'fritzbox',
				'name': 'Fritz!Box',
				'url': BASE_URL + reverse('ddns:host-update-fritzbox', kwargs = {
					'pk': self.get_object().pk,
					'token': self.get_object().token,
				}) + "?ipv4=<ipaddr>&ipv6=<ip6addr>"
			},
		]
		return context
	

class HostRenewTokenView(CrispyUpdateView):
	model = models.DynHost
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

def update_host(pk, token, ipv4 = None, ipv6 = None):
	host = None
	try:
		host = models.Host.objects.get(pk = pk, token = token)
	except:
		return HttpResponseBadRequest('Host not found.')
	
	u = dnsutils.Updater(settings.BIND_SERVER_NAME, host.zone.zone.name)
	u.delete_host(host.name)
	if ipv4:
		u.add({
			'rname': host.name,
			'rttl': 60,
			'rtype': 'A',
			'rdata': ipv4
		})
	if ipv6:
		u.add({
			'rname': host.name,
			'rttl': 60,
			'rtype': 'AAAA',
			'rdata': ipv6
		})
	response = u.send()
	host.last_update = timezone.now()
	host.save()
	return HttpResponse("Response: {}".format(response))

@method_decorator(csrf_exempt, name='dispatch')
class HostUpdateFritzboxView(View):
	http_method_names = ['get', 'post']

	def get(self, request, *args, **kwargs):
		return update_host(kwargs['pk'], kwargs['token'], request.GET.get('ipv4', None), request.GET.get('ipv6', None))
	def post(self, request, *args, **kwargs):
		return update_host(kwargs['pk'], kwargs['token'], request.POST.get('ipv4', None), request.POST.get('ipv6', None))
