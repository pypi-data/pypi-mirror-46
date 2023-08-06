{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.height is not none %}
    :height: {{ obj.height }}px
{%- endif %}
{%- if obj.width is not none %}
    :width: {{ obj.width }}px
{%- endif %}
{%- if obj.alt_text is not none %}
    :alt: {{ obj.alt_text }}
{%- endif %}
{%- if obj.align is not none %}
    :align: {{ obj.align }}
{%- endif %}
{% endblock %}