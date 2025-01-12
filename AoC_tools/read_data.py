import re


def read_data(file, numbers=True, by_block=False, split=None):
    """ Reads a typical input file of the AoC
    :param file: name of the file (with the path)
    :param numbers:
    :param by_block:
    :param split: a string that will be used to split the values in a given line of the input file
    :return: a list of data to use in the function (list of numbers, of strings, of lists...)
    """
    with open(file, 'r') as fic:
        if by_block:
            if split is not None:
                raise Exception("The split is not implemented yet for the reading by blocks.")
            if numbers:
                data = [[int(x) for x in block.split('\n') if x.isdigit()] for block in fic.read().split('\n\n')]
            else:
                data = [[x for x in block.split('\n') if x != ''] for block in fic.read().split('\n\n')]
        else:
            if split is None:
                if numbers:
                    data = [int(x) for x in fic.read().split('\n')[:-1] if x != '']
                else:
                    data = [x for x in fic.read().split('\n')[:-1]]
            else:
                if numbers:
                    data = [
                        [int(x) if x.isdigit() else x for x in line.split(split)]
                        for line in fic.read().split('\n')[:-1]
                    ]
                else:
                    data = [line.split(split) for line in fic.read().split('\n')[:-1]]
    return data


def smart_split(data, pattern):
    if type(data) == str:
        return re.split(pattern, data)
    else:
        return [re.split(pattern, line) for line in data]