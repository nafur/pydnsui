import datetime
from django import template

register = template.Library()

@register.simple_tag
def server_row(server, only_local = None):
	if only_local is True and server.remote is not None:
		return ""
	if only_local is False and server.remote is None:
		return ""
	s = """
	<tr{% if not server.enabled %} class="table-secondary"{% endif %}>
		<th>
			{% enabled_icon server %}
			{% if server.remote %}
			<a href="{{ server.get_absolute_url }}"> {{ server.name }}</a> @ <a href="{{ server.remote.get_absolute_url }}">{{ server.remote.name }}</a>
			{% else %}
				{% fa5_icon 'home' %} <a href="{{ server.get_absolute_url }}"> {{ server.name }}</a>
			{% endif %}
		</th>
		<td><code>{{ server.ipv4 }}</code></td>
		<td><code>{{ server.ipv6 }}</code></td>
		<td><code>{{ server.nameserver }}</code></td>
		<td>{% show_owner server %}</td>
		<td>
			{% if server.enabled %}
				<a class="btn btn-sm btn-secondary" href="{% url 'fed:server-disable' server.pk %}">{% fa5_icon 'ban' %} disable</a>
			{% else %}
				<a class="btn btn-sm btn-primary" href="{% url 'fed:server-enable' server.pk %}">{% fa5_icon 'check' %} enable</a>
			{% endif %}
			<a class="btn btn-sm btn-primary" href="{% url 'fed:server-edit' server.pk %}">{% fa5_icon 'edit' %} edit</a>
			<a class="btn btn-sm btn-primary" href="{% url 'fed:server-delete' server.pk %}">{% fa5_icon 'trash' %} delete</a>
		</td>
	</tr>
	"""
	return template.Template("{% load fontawesome_5 %}{% load helpers %}" + s).render(template.Context({'server': server}))