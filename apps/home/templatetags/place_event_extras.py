from apps.home.templatetags import miscellaneous_extras
from django import template

register = template.Library()


@register.filter
def get_values_from_dicts(dict, key):
    # print(dict)
    return miscellaneous_extras.get_values_of_dicts_within_dict(dict, key, "placeID")
