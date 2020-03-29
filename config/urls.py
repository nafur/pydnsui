from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path, reverse_lazy
from django.views.generic import *

from pydnsui.views import *
from . import forms, models, views

urlpatterns = [
	path('',
		login_required(TemplateView.as_view(
			template_name = "config/index.html"
		)),
		name='index'
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
				fields = ['name', 'enabled', 'admins'],
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
				fields = ['name', 'enabled', 'admins'],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-edit',
	),
	path('zone/<int:pk>/disable',
		login_required(
			DisableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('zone-list')
			)
		),
		name = 'zone-disable',
	),
	path('zone/<int:pk>/enable',
		login_required(
			EnableView.as_view(
				model = models.Zone,
				redirect_url = reverse_lazy('zone-list')
			)
		),
		name = 'zone-enable',
	),
	path('zone/<int:pk>/delete', 
		login_required(
			CrispyDeleteView.as_view(
				model = models.Zone,
				success_url = reverse_lazy('zone-list'),
			)
		),
		name = 'zone-delete',
	),
	path('record/<int:zone>/create',
		login_required(
			views.RecordCreateView.as_view(
				form_submit_text = 'Submit',
			)
		),
		name = 'record-create',
	),
	path('record/<int:pk>/edit', 
		login_required(
			CrispyUpdateView.as_view(
				model = models.Record,
				fields = ['rname', 'rttl', 'rclass', 'rtype', 'rdata'],
				form_submit_text = 'Submit',
			)
		),
		name = 'record-edit',
	),
	path('record/<int:pk>/delete', 
		login_required(
			views.RecordDeleteView.as_view()
		),
		name = 'record-delete',
	),
	path('deploy',
		login_required(
			views.DeployView.as_view()
		),
		name = 'deploy',
	)
]
