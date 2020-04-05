zone "{{ zone.name }}" {
	type master;
	file "{{ basedir }}db.{{ zone.name }}";
	allow-transfer {
		10.0.0.0/16; # docker network
		{% for s in slaves %}
		{{ s.ipv4 }}; {{ s.ipv6 }}; # {{ s.name }}
		{% endfor %}
	};
	allow-query { any; };
	zone-statistics yes;
	update-policy local;
	key-directory "/etc/bind/keys";
	auto-dnssec maintain;
	inline-signing yes;
};
