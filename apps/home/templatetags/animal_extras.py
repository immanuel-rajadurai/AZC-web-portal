from django import template
from apps.home.services import animal_services

register = template.Library()


@register.filter
def get_animal_name(animal_id):
    tmp = animal_services.get_animal(animal_id)

    if tmp:
        return tmp["name"]
    return "Undefined"
