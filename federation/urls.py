from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path, reverse_lazy
from django.views.generic import *

from pydnsui.views import *
from pydnsui.decorators import *
from . import models, views

app_name = 'fed'
urlpatterns = [
	path('remotes',
		login_required(
			ListView.as_view(model = models.Remote)
		),
		name = 'remote-list',
	),
	path('remotes/create',
		login_required(
			CrispyCreateView.as_view(
				model = models.Remote,
				fields = [ 'name', 'enabled', 'auth_token', 'pull_url', 'pull_token'],
				form_submit_text = 'Submit',
			)
		),
		name = 'remote-create',
	),
	path('remotes/<int:pk>',
		owner_required(
			DetailView.as_view(model = models.Remote)
		),
		name = 'remote-detail',
	),
	path('remotes/<int:pk>/edit',
		owner_required(
			CrispyUpdateView.as_view(
				model = models.Remote,
				fields = [ 'name', 'enabled', 'owners', 'auth_token', 'pull_url', 'pull_token'],
				form_submit_text = 'Submit',
			)
		),
		name = 'remote-edit',
	),
	path('remotes/<int:pk>/delete',
		owner_required(
			CrispyDeleteView.as_view(
				model = models.Remote,
				success_url = reverse_lazy('fed:remote-list'),
			)
		),
		name = 'remote-delete',
	),
	path('remotes/<int:pk>/disable',
		owner_required(
			DisableView.as_view(
				model = models.Remote,
				redirect_url = reverse_lazy('fed:remote-list')
			)
		),
		name = 'remote-disable',
	),
	path('remotes/<int:pk>/enable',
		owner_required(
			EnableView.as_view(
				model = models.Remote,
				redirect_url = reverse_lazy('fed:remote-list')
			)
		),
		name = 'remote-enable',
	),
	path('remotes/<int:pk>/pull',
		owner_required(
			views.PullManualView.as_view()
		),
		name = 'remote-pull',
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
				fields = [ 'name', 'enabled', 'ipv4', 'ipv6', 'nameserver'],
				form_submit_text = 'Submit',
			)
		),
		name = 'server-create',
	),
	path('server/<int:pk>',
		owner_required(
			DetailView.as_view(model = models.Server)
		),
		name = 'server-detail',
	),
	path('server/<int:pk>/edit',
		owner_required(
			CrispyUpdateView.as_view(
				model = models.Server,
				fields = [ 'name', 'enabled', 'owners', 'ipv4', 'ipv6', 'nameserver'],
				form_submit_text = 'Submit',
			)
		),
		name = 'server-edit',
	),
	path('server/<int:pk>/delete',
		owner_required(
			CrispyDeleteView.as_view(
				model = models.Server,
				success_url = reverse_lazy('fed:server-list'),
			)
		),
		name = 'server-delete',
	),
	path('server/<int:pk>/disable',
		owner_required(
			DisableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list')
			)
		),
		name = 'server-disable',
	),
	path('server/<int:pk>/enable',
		owner_required(
			EnableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list')
			)
		),
		name = 'server-enable',
	),
	path('server/<int:pk>/disable-pull',
		owner_required(
			DisableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list'),
				property_name = 'pull_enabled'
			)
		),
		name = 'server-disable-pull',
	),
	path('server/<int:pk>/enable-pull',
		owner_required(
			EnableView.as_view(
				model = models.Server,
				redirect_url = reverse_lazy('fed:server-list'),
				property_name = 'pull_enabled'
			)
		),
		name = 'server-enable-pull',
	),
	path('server/<int:pk>/pull',
		owner_required(
			views.PullManualView.as_view()
		),
		name = 'server-pull',
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
					'name', 'enabled', 'main', 'subordinates_all', 'subordinates'
				],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-create',
	),
	path('zone/<int:pk>',
		owner_required(
			DetailView.as_view(model = models.Zone)
		),
		name = 'zone-detail',
	),
	path('zone/<int:pk>/edit',
		owner_required(
			CrispyUpdateView.as_view(
				model = models.Zone,
				fields = [
					'name', 'enabled', 'owners', 'main', 'subordinates_all', 'subordinates'
				],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-edit',
	),
	path('zone/<int:pk>/disable',
		owner_required(
			DisableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('fed:zone-list')
			)
		),
		name = 'zone-disable',
	),
	path('zone/<int:pk>/enable',
		owner_required(
			EnableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('fed:zone-list')
			)
		),
		name = 'zone-enable',
	),
	path('export/zones',
		views.ExportZonesView.as_view(),
		name = 'export-zones',
	),
]