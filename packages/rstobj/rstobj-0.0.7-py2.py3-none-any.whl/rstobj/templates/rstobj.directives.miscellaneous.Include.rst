{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.start_line is not none %}
    :start_line: {{ obj.start_line }}
{%- endif %}
{%- if obj.end_line is not none %}
    :end_line: {{ obj.end_line }}
{%- endif %}
{%- if obj.start_after is not none %}
    :start_after: {{ obj.start_after }}
{%- endif %}
{%- if obj.end_before is not none %}
    :end_before: {{ obj.end_before }}
{%- endif %}
{%- if obj.literal is not none %}
    :literal:
{%- endif %}
{%- if obj.code is not none %}
    :code: {{ obj.code }}
{%- endif %}
{%- if obj.number_lines is not none %}
    :number_lines: {{ obj.number_lines }}
{%- endif %}
{%- if obj.encoding is not none %}
    :encoding: {{ obj.encoding }}
{%- endif %}
{%- if obj.tab_width is not none %}
    :tab_width: {{ obj.tab_width }}
{%- endif %}
{% endblock %}