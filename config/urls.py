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
	path('zones',
		login_required(
			ListView.as_view(model = models.Zone)
		),
		name = 'zone-list',
	),
	path('zones/create', 
		login_required(
			CrispyCreateView.as_view(
				model = models.Zone,
				fields = ['name', 'admins'],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-create',
	),
	path('zones/deploy',
		login_required(
			views.ZoneDeployView.as_view()
		),
		name = 'zone-deploy',
	),
	path('zones/<int:pk>',
		login_required(
			views.ZoneDetailView.as_view()
		),
		name = 'zone-detail',
	),
	path('zones/<int:pk>/edit', 
		login_required(
			CrispyUpdateView.as_view(
				model = models.Zone,
				fields = ['name', 'admins'],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-edit',
	),
	path('zones/<int:pk>/delete', 
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
			views.RecordCreateView.as_view()
		),
		name = 'record-create',
	),
	path('record/<int:zone>/edit/<str:serialized>', 
		login_required(
			views.RecordUpdateView.as_view()
		),
		name = 'record-edit',
	),
	path('record/<int:zone>/delete/<str:serialized>', 
		login_required(
			views.RecordDeleteView.as_view()
		),
		name = 'record-delete',
	),
]
