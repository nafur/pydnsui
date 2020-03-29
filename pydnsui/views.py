from django.db.models import Field
from django.views.generic import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

def default_layout(form, submit_text):
	fields = [f for f,_ in form.base_fields.items()]
	helper = FormHelper()
	helper.layout = Layout(*fields)
	if isinstance(submit_text, tuple):
		helper.add_input(Submit(*submit_text))
	else:
		helper.add_input(Submit('save', submit_text))
	return helper

class FormHelperMixin(object):
	form_helper = None
	form_submit_text = 'Submit'
	form_helper_name = 'form_helper'

	def get_context_data(self, **kwargs):
		if self.form_helper is not None:
			kwargs[self.form_helper_name] = self.form_helper
		else:
			form = self.get_form_class()
			kwargs[self.form_helper_name] = default_layout(form, self.form_submit_text)
		return super(FormHelperMixin, self).get_context_data(**kwargs)

class CrispyCreateView(FormHelperMixin, CreateView):
	pass
class CrispyUpdateView(FormHelperMixin, UpdateView):
	pass
class CrispyDeleteView(DeleteView):
	pass

class PropertyModifierView(RedirectView):
	permanent = False
	model = None
	property_name = None
	property_value = None
	redirect_url = None

	def get_redirect_url(self, *args, **kwargs):
		obj = self.model.objects.get(pk = kwargs['pk'])
		obj.__dict__[self.property_name] = self.property_value
		obj.save()
		return self.redirect_url

class DisableView(PropertyModifierView):
	property_name = 'enabled'
	property_value = False

class EnableView(PropertyModifierView):
	property_name = 'enabled'
	property_value = True
