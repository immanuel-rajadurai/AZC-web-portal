from django import template

register = template.Library()


@register.filter
def get_list_from_dict(dictionary, key):
    tmp = dictionary.get(key)
    # print("tmp:", tmp)

    tmp2 = []

    if isinstance(tmp, dict):
        for key, value in tmp.items():
            # print("value: ", value)
            tmp2.append(value)

    return tmp2
