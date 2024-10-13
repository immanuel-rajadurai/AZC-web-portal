def split_tags(tags):
    result = tags.strip().split(",")

    lst = []
    for r in result:
        lst.append(r.strip())

    return lst
