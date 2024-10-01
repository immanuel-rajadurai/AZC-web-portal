from django import template
from apps.home.services import place_services

register = template.Library()


@register.filter
def get_place_name(place_id):
    return place_services.get_place(place_id)["name"]
