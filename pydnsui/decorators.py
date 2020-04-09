from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def owner_required(func, model = None, pk_field = 'pk'):
	if model is None:
		model = func.view_class.model
	def check_and_call(request, *args, **kwargs):
		try:
			obj = model.objects.get(pk = kwargs[pk_field])
		except Exception as e:
			print(e)
		if obj is not None:
			if not obj.is_owned():
				raise PermissionDenied()
		return func(request, *args, **kwargs)
	return login_required(check_and_call)