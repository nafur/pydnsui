# Include all configs from here.

{% for filename in zones %}
include "{{ filename }}";
{% endfor %}
