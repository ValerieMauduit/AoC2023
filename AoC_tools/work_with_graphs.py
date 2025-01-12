class AocGraph:
    def __init__(self, paths):
        self.nodes = list(set([x[0] for x in paths] + [x[1] for x in paths]))
        sorted_paths = []
        for path in paths:
            path.sort()
            if path not in sorted_paths:
                sorted_paths += [path]
        self.paths = sorted_paths
        self.forbidden = []
        self.neighbours = {node: [] for node in self.nodes}
        for path in sorted_paths:
            self.neighbours[path[0]] += [path[1]]
            self.neighbours[path[1]] += [path[0]]

    def get_neighbours(self, node, available_only=False):
        if available_only:
            forbidden = self.forbidden
        else:
            forbidden = []
        if node not in self.nodes:
            return []
        return [neighbour for neighbour in self.neighbours[node] if neighbour not in forbidden]

    def forbid_node(self, node):
        self.forbidden += [node]

    def distance(self, node1, node2, available_only=False):
        if (node1 not in self.nodes) | (node2 not in self.nodes) | \
                (available_only & ((node1 in self.forbidden) | (node2 in self.forbidden))):
            return None
        distances = {node1: 0}
        not_found = True
        all_checked = False
        to_check = [node1]
        while not_found & (not all_checked):
            next_checks = []
            for node in to_check:
                for neighbour in self.get_neighbours(node, available_only):
                    if neighbour not in distances:
                        next_checks += [neighbour]
                        distances[neighbour] = distances[node] + 1
            not_found = (node2 not in distances)
            all_checked = (len(distances.keys()) == len(self.nodes))
            to_check = next_checks
        if not_found:
            return None
        return distances[node2]


def count_paths(graph, from_node, to_node, no_loop=True, forbidden=None):
    # This one is recursive
    if forbidden is None:
        forbidden = []
    if from_node == to_node:
        return 1
    else:
        total = 0
        for neighbour in graph.get_neighbours(from_node, True):
            if neighbour not in forbidden:
                if no_loop:
                    branch_forbidden = forbidden + [from_node]
                else:
                    branch_forbidden = forbidden
                total += count_paths(graph, neighbour, to_node, no_loop, branch_forbidden)
        return total


def next_paths(path, graph):
    paths = []
    for neighbour in graph.get_neighbours(path['path'][-1]):
        if neighbour not in path['forbidden']:
            paths += [{'path': path['path'] + [neighbour], 'forbidden': path['forbidden']}]
    return paths


def all_paths(graph, from_node, to_node, forbid_function=None):
    # This one is deep search first (favourite)
    in_progress = [{'path': [from_node], 'forbidden': []}]
    paths = []
    while len(in_progress) > 0:
        if in_progress[0]['path'][-1] == to_node:
            paths += in_progress[0]['path']
            in_progress = in_progress[1:]
        else:
            forbidden = in_progress[0]['forbidden']
            if forbid_function(from_node):
                # If the forbid_function is too complicated: copy/paste all the code and do it inside
                forbidden += [from_node]
            in_progress = next_paths({'path': in_progress[0]['path'], 'forbidden': forbidden}, graph) + in_progress[1:]
    return paths
