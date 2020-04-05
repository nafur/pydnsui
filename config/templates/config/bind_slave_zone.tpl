zone "{{ zone.name }}" {
	type slave;
	file "{{ basedir }}db.slave_{{ zone.name }}";
	masters {
		{{ zone.master.ipv4 }}; {{ zone.master.ipv6 }}; # {{ zone.master.name }}
	};
	allow-query { any; };
};
