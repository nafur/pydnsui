zone "{{ zone.name }}" {
	type master;
	file "{{ basedir }}db.{{ zone.name }}";
	allow-transfer {
		10.0.0.0/16; # docker network
		{% for s in slaves %}
		{{ s.ipv4 }}; {{ s.ipv6 }}; # {{ s.name }}
		{% endfor %}
	};
	allow-update {
		10.0.0.0/16; # docker network
	};
	allow-query { any; };
	zone-statistics yes;
	key-directory "/etc/bind/keys";
	auto-dnssec maintain;
	inline-signing yes;
};
