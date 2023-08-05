import json

from django import template

register = template.Library()


@register.filter
def beautify_json(j):
    return json.dumps(j, indent=2, sort_keys=True)
