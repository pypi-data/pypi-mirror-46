{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.header %}
    :header-rows: 1
{%- else %}
    :header-rows: 0
{%- endif %}
{%- if obj.index %}
    :stub-columns: 1
{%- else %}
    :stub-columns: 0
{%- endif %}
{%- if obj.align is not none %}
    :align: {{ obj.align }}
{%- endif %}
{% for row in obj.data %}
    {%- for item in row %}
    {%- if loop.index0 == 0 %}
    * - {{ obj.str_or_render(item, indent=2, first_line_indent=0) }}
    {%- else %}
      - {{ obj.str_or_render(item, indent=2, first_line_indent=0) }}
    {%- endif %}
    {%- endfor %}
{%- endfor %}
{% endblock %}