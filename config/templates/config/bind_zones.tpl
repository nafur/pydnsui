{% for zone in master_zones %}
zone "{{ zone.name }}" {
	type master;
	file "/etc/bind/zones/db.{{ zone.name }}";
{% if zone.slaves %}
	allow-transfer {
		{% for s in zone.slaves %}
		{{ s.ipv4 }}; {{ s.ipv6 }}; # {{ s.name }}
		{% endfor %}
	};
	allow-query { any; };
{% endif %}
	zone-statistics yes;
	update-policy local;
	key-directory "/etc/bind/keys";
	auto-dnssec maintain;
	inline-signing yes;
};
{% endfor %}
{% for zone in slave_zones %}
zone "{{ zone.name }}" {
	type slave;
	file "/etc/bind/zones/db.{{ zone.name }}";
	masters {
		{{ zone.master.ipv4 }}; {{ zone.master.ipv6 }}; # {{ zone.master.name }}
	};
	allow-query { any; };
};
{% endfor %}