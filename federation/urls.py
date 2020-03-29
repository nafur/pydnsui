from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path, reverse_lazy
from django.views.generic import *

from pydnsui.views import *
from . import models, views

app_name = 'fed'
urlpatterns = [
	path('server',
		login_required(
			ListView.as_view(model = models.Server)
		),
		name = 'server-list',
	),
	path('server/create', 
		login_required(
			CrispyCreateView.as_view(
				model = models.Server,
				fields = [ 'name', 'enabled', 'admins', 'push_url', 'push_enabled', 'ipv4', 'ipv6', 'token' ],
				form_submit_text = 'Submit',
			)
		),
		name = 'server-create',
	),
	path('server/<int:pk>',
		login_required(
			DetailView.as_view(model = models.Server)
		),
		name = 'server-detail',
	),
	path('server/<int:pk>/edit',
		login_required(
			CrispyUpdateView.as_view(
				model = models.Server,
				fields = [ 'name', 'enabled', 'admins', 'push_url', 'push_enabled', 'ipv4', 'ipv6', 'token' ],
				form_submit_text = 'Submit',
			)
		),
		name = 'server-edit',
	),
	path('server/<int:pk>/disable',
		login_required(
			DisableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list')
			)
		),
		name = 'server-disable',
	),
	path('server/<int:pk>/enable',
		login_required(
			EnableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list')
			)
		),
		name = 'server-enable',
	),
	path('server/<int:pk>/disable-push',
		login_required(
			DisableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list'),
				property_name = 'push_enabled'
			)
		),
		name = 'server-disable-push',
	),
	path('server/<int:pk>/enable-push',
		login_required(
			EnableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list'),
				property_name = 'push_enabled'
			)
		),
		name = 'server-enable-push',
	),
	path('zone',
		login_required(
			ListView.as_view(model = models.Zone)
		),
		name = 'zone-list',
	),
	path('zone/create', 
		login_required(
			CrispyCreateView.as_view(
				model = models.Zone,
				fields = [
					'name', 'enabled', 'master', 'slaves_all', 'slaves'
				],
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
	path('zone/<int:pk>/edit',
		login_required(
			CrispyUpdateView.as_view(
				model = models.Zone,
				fields = [
					'name', 'enabled', 'master', 'slaves_all', 'slaves'
				],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-edit',
	),
	path('zone/<int:pk>/disable',
		login_required(
			DisableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('fed:zone-list')
			)
		),
		name = 'zone-disable',
	),
	path('zone/<int:pk>/enable',
		login_required(
			EnableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('fed:zone-list')
			)
		),
		name = 'zone-enable',
	),
]