{%- for item in obj.items %}
{{ obj.start_num + loop.index0 }}. {{ item }}
{%- endfor %}
