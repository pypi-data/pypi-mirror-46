:gitlab_url: https://gitlab.com/tud-mst/ptvpy/blob/master/src/{{ module | replace(".", "/") }}.py

{{ name | escape | underline }}

in module :mod:`{{ module }}`.

{% if objtype == "class" %}
.. autoclass:: {{ fullname }}
   :members:
{% else %}
.. auto{{ objtype }}:: {{ fullname }}
{% endif %}
