;; db.{{ zone.name }}
$TTL 5m

@ IN SOA {{ zone.name }}. noreply.{{ zone.name }}. (
	{% now "ymdHi" %} ; serial number
	30m ; refresh 
	5m ; update retry
	1d ; expiry
	1m ; minimum
)

{% for ns in zone.get_nameservers %}
{{ zone.name}}. IN NS {{ ns }}
{% endfor %}
