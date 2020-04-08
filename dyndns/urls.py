from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path, reverse_lazy
from django.views.generic import *

from pydnsui.views import *
from . import forms, models, views

app_name = 'ddns'
urlpatterns = [
	path('zones',
		login_required(
			ListView.as_view(model = models.Zone)
		),
		name = 'zone-list',
	),
	path('zone/create',
		login_required(
			CrispyCreateView.as_view(
				model = models.Zone,
				fields = [ 'zone', 'enabled'],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-create',
	),
	path('zone/<int:pk>',
		login_required(
			DetailView.as_view(model = models.Zone)
		),
		name = 'zone-detail',
	),
	path('zone/<int:pk>/delete',
		login_required(
			CrispyDeleteView.as_view(
				model = models.Zone,
				success_url = reverse_lazy('ddns:zone-list'),
			)
		),
		name = 'zone-delete',
	),
	path('zone/<int:pk>/disable',
		login_required(
			DisableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('ddns:zone-list')
			)
		),
		name = 'zone-disable',
	),
	path('zone/<int:pk>/enable',
		login_required(
			EnableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('ddns:zone-list')
			)
		),
		name = 'zone-enable',
	),
	path('zone/<int:pk>/create-host',
		login_required(
			views.HostCreateView.as_view()
		),
		name = 'host-create',
	),
	path('host/<int:pk>/delete',
		login_required(
			views.HostDeleteView.as_view()
		),
		name = 'host-delete',
	),
	path('host/<int:pk>/renew-token',
		login_required(
			views.HostRenewTokenView.as_view()
		),
		name = 'host-renew-token',
	),
	path('host/<int:pk>/usage',
		login_required(
			views.HostDetailView.as_view()
		),
		name = 'host-usage',
	),
	path('fritzbox/<int:pk>/<str:token>',
		views.HostUpdateFritzboxView.as_view(),
		name = 'host-update-fritzbox',
	),
]