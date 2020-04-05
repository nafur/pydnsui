import datetime
import subprocess
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def enabled_icon(obj, property_name = 'enabled'):
	if obj.__dict__[property_name]:
		t = "{% fa5_icon 'check' title='enabled' %}"
	else:
		t = "{% fa5_icon 'ban' title='disabled' %}"
	return template.Template("{% load fontawesome_5 %}" + format(t)).render(template.Context())

@register.simple_tag
def git_version():
	describe = subprocess.run(['git', 'describe', '--always'], capture_output = True, cwd = settings.BASE_DIR).stdout.decode('utf8')
	hash = subprocess.run(['git', 'log', '-1', '--format=%h', '--date=relative'], capture_output = True, cwd = settings.BASE_DIR).stdout.decode('utf8')
	when = subprocess.run(['git', 'log', '-1', '--format=%cd', '--date=relative'], capture_output = True, cwd = settings.BASE_DIR).stdout.decode('utf8')
	return mark_safe("git <a href=\"https://github.com/nafur/pydnsui/commit/{}\">version {}</a> from {}".format(describe, hash, when))
