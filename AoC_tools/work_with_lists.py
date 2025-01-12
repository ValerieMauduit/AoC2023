import itertools


def sliding_windows(data, size=3):
    # Returns the list of the sub-lists of a given span in an ordered list
    if type(data) == str:
        return [''.join([data[n + p] for p in range(size)]) for n in range(len(data) - size + 1)]
    else:
        return [[data[n + p] for p in range(size)] for n in range(len(data) - size + 1)]


def str_to_list(string):
    # Returns a string in a list of characters
    return [x for x in string]


def positions(value, in_list):
    # Returns all the indexes of a value into a list, with no error if the value is not in the list
    indexes = []
    increment = 0
    while value in in_list:
        value_index = in_list.index(value)
        indexes += [value_index + increment]
        in_list = in_list[(value_index + 1):]
        increment = value_index + increment + 1
    return indexes


def count_value(value, in_list):
    # Counts the occurrences of a given value in a list
    return sum([x == value for x in in_list])


def most_common(in_list, values=None):
    # What is the most common value and how many occurrences?
    result = [None, 0]
    if values is None:
        values = set(in_list)
    for value in values:
        count = count_value(value, in_list)
        if count > result[1]:
            result = [value, count]
    return result


def least_common(in_list, values=None):
    # What is the least common present value and how many occurrences?
    result = [None, len(in_list) + 1]
    if values is None:
        values = set(in_list)
    for value in values:
        count = count_value(value, in_list)
        if count < result[1]:
            result = [value, count]
    return result


def merge_lists(list1, list2):
    return [x for x in itertools.chain(*[[list1[n], list2[n]] for n in range(len(list1))])]


def transpose(list_of_lists):
    return [[x[n] for x in list_of_lists] for n in range(len(list_of_lists[0]))]


def is_included(compared_list, parent_list):
    return any(
        compared_list == parent_list[x:x + len(compared_list)] for x in range(len(parent_list) - len(compared_list) + 1)
    )
