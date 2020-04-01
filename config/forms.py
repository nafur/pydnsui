from django import forms

from . import models

class RecordForm(forms.Form):
	rname = forms.CharField(
		max_length = 255,
		label = 'Record name',
	)
	rttl = forms.IntegerField(
		initial = 24*3600,
		label = 'TTL',
	)
	rclass = forms.ChoiceField(
		choices = [("IN", "IN"), ("CH", "CH"), ("HS", "HS"), ("CS", "CS")],
		initial = 'IN',
		label = 'Class',
	)
	rtype = forms.CharField(
		max_length = 16,
		initial = 'A',
		label = 'Type',
	)
	rdata = forms.CharField(
		widget = forms.Textarea,
		label = 'Data',
	)
