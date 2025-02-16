def get_ids_from_filter(lst, key):
    tmp = []

    if lst:
        for item in lst:
            tmp2 = item[key]
            tmp.append(tmp2)

    return tmp

def split_tags(tags):
    result = tags.strip().split(",")

    lst = []
    for r in result:
        lst.append(r.strip())

    return lst