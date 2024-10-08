from django import template

register = template.Library()


def get_list_from_dict(dictionary, key, key2):
    tmp = dictionary.get(key)
    # print("tmp:", tmp)

    tmp2 = []

    for dict in tmp:
        # print("dict: ", dict)
        tmp2.append(dict[key2])

    return tmp2


def get_values_of_dicts_within_dict(dict, key, key2):
    lst = get_list_from_dict(dict, key, key2)

    tmp = []
    for dict in lst:
        tmp2 = dict[key2]
        # print("tmp2: ", tmp2)
        # tmp.append(py)

    return tmp
