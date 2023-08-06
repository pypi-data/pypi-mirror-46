{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.depth is not none %}
    :depth: {{ obj.depth }}
{%- endif %}
{%- if obj.local %}
    :local:
{%- endif %}
{%- if obj.backlinks is not none %}
    :backlinks: {{ obj.backlinks }}
{%- endif %}
{% endblock %}