import datetime
from django import template

register = template.Library()

@register.simple_tag
def enabled_icon(obj):
	if obj.enabled:
		t = "{% fa5_icon 'check' title='enabled' %}"
	else:
		t = "{% fa5_icon 'ban' title='disabled' %}"
	return template.Template("{% load fontawesome_5 %}" + format(t)).render(template.Context())