from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.views.generic import *

from pydnsui.views import *
from pydnsui.decorators import *
from . import forms, models, views

app_name = 'config'
urlpatterns = [
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
				fields = ['name'],
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
		owner_required(
				views.ZoneDetailView.as_view()
		),
		name = 'zone-detail',
	),
	path('zones/<int:pk>/edit',
		owner_required(
			CrispyUpdateView.as_view(
				model = models.Zone,
				fields = ['name', 'owners'],
				form_submit_text = 'Submit',
			)
		),
		name = 'zone-edit',
	),
	path('zones/<int:pk>/delete', 
		owner_required(
			CrispyDeleteView.as_view(
				model = models.Zone,
				success_url = reverse_lazy('config:zone-list'),
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
		owner_required(
			views.RecordUpdateView.as_view(),
			model = models.Zone,
			pk_field = 'zone',
		),
		name = 'record-edit',
	),
	path('record/<int:zone>/delete/<str:serialized>', 
		owner_required(
			views.RecordDeleteView.as_view(),
			model = models.Zone,
			pk_field = 'zone',
		),
		name = 'record-delete',
	),
]
