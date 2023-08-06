.. {{ obj.meta_directive_keyword }}:: {{ obj.arg }}
    {%- if obj.class_ is not none %}
    :class: {{ obj.class_ }}
    {%- endif %}
    {%- if obj.name is not none %}
    :name: {{ obj.name }}
    {%- endif %}
    {%- block other %}{% endblock %}
