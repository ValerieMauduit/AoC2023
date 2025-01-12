def update_dict(dictionary, key, value, cumulative=False):
    if not cumulative:
        value = [value]
    if key in dictionary.keys():
        dictionary[key] += value
    else:
        dictionary[key] = value
    return dictionary
