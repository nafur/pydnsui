from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path, reverse_lazy
from django.views.generic import *

from pydnsui.views import *
from . import models, views

app_name = 'fed'
urlpatterns = [
	path('remote',
		login_required(
			ListView.as_view(model = models.Remote)
		),
		name = 'remote-list',
	),
	path('remote/create', 
		login_required(
			CrispyCreateView.as_view(
				model = models.Remote,
				fields = [
					'name', 'enabled', 'url', 'importer'
				],
				form_submit_text = 'Submit',
			)
		),
		name = 'remote-create',
	),
	path('remote/<int:pk>/edit',
		login_required(
			CrispyUpdateView.as_view(
				model = models.Remote,
				fields = [
					'name', 'enabled', 'url', 'importer'
				],
				form_submit_text = 'Submit',
				success_url = reverse_lazy('fed:remote-list'),
			)
		),
		name = 'remote-edit',
	),
	path('remote/<int:pk>/disable',
		login_required(
			DisableView.as_view(
				model = models.Remote,
				redirect_url = reverse_lazy('fed:remote-list')
			)
		),
		name = 'remote-disable',
	),
	path('remote/<int:pk>/enable',
		login_required(
			EnableView.as_view(
				model = models.Remote,
				redirect_url = reverse_lazy('fed:remote-list')
			)
		),
		name = 'remote-enable',
	),
	path('remote/<int:pk>/import',
		login_required(
			views.RemoteManualImportView.as_view()
		),
		name = 'remote-import',
	),
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
				fields = [
					'name', 'admins', 'ipv4', 'ipv6', 'token'
				],
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