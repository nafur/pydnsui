;; db.{{ zone.name }}
$TTL 5m

@ IN SOA {{ zone.name }}. noreply.{{ zone.name }}. (
	{% now "ymdHi" %} ; serial number
	30m ; refresh 
	5m ; update retry
	1d ; expiry
	1m ; minimum
)

{% for ns in zone.nameserver %}
{{ zone.name}}. IN NS {{ ns.nameserver }}
{% endfor %}

{% for r in zone.records.all %}
{{ r.rname|ljust:"10" }} {{ r.rttl|rjust:"6" }} {{ r.rclass|ljust:"2" }} {{ r.rtype|ljust:"5" }} {{ r.rdata }}
{% endfor %}