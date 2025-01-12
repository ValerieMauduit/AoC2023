import itertools
import numpy as np

class AocMap:
    def __init__(self, data, position=None, origin=None, numbers=False):
        # Instantiation - Create a map from a data input of type "AoC input file data"
        # Attributes:
        # map: represents the map as a list of lists (kind of numpy array)
        #       x goes from left to right, y from top to bottom
        # origin: coordinates [x, y] of the top left point of the map
        # x, y: coordinates of the point where we are (position)
        # width, height
        if numbers:
            self.map = [[int(x) for x in line] for line in data]
        else:
            self.map = [[x for x in line] for line in data]
        if origin is None:
            self.origin = [0, 0]
        else:
            self.origin = origin
        if position is None:
            self.x, self.y = self.origin[0], self.origin[1]
        else:
            self.x, self.y = position[0], position[1]
        self.width = len(data[0])
        self.height = len(data)

    @classmethod
    def empty_from_size(cls, width, height):
        # Constructor - Create an empty map, full of '.' defining only its width and height
        data = ['.' * width for _ in range(height)]
        return cls(data)

    @classmethod
    def from_coord(cls, coordinates, x_min=None, y_min=None, x_max=None, y_max=None):
        # Constructor - Create a map made of '.' for the empty places and '#' for all the coordinates that are entered
        # in the parameters.
        # Optional inputs: x_min, x_max, y_min, y_max, that will define the size of the map + the origin.
        if x_min is None:
            x_min = min([coord[0] for coord in coordinates])
        if y_min is None:
            y_min = min([coord[1] for coord in coordinates])
        if x_max is None:
            x_max = max([coord[0] for coord in coordinates])
        if y_max is None:
            y_max = max([coord[1] for coord in coordinates])
        map_from_coord = cls.empty_from_size(x_max - x_min + 1, y_max - y_min + 1)
        map_from_coord.origin = [x_min, y_min]
        map_from_coord.set_points(coordinates)
        return map_from_coord

    def copy(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def display(self, numbers=False):
        # Method to display the map in the terminal
        if numbers:
            for line in self.map:
                print("".join([f"{x: >3d}" for x in line]))
        else:
            for line in self.map:
                print("".join([str(x) for x in line]))

    def get_position(self):
        # Method to get the position coordinates
        return [self.x, self.y]

    def set_position(self, position):
        # Method to change x and y by indicating the new position
        self.x, self.y = position[0], position[1]

    def one_move(self, direction):
        # Method to change the position, but by indicating a direction (like 'U') and move for 1 cell
        displacements = {
            'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0],
            'N': [0, -1], 'S': [0, 1], 'W': [-1, 0], 'E': [1, 0]
        }
        if direction in displacements:
            self.x += displacements[direction][0]
            self.y += displacements[direction][1]
            self.x = min([max([self.origin[0], self.x]), self.origin[0] + self.width - 1])
            self.y = min([max([self.origin[1], self.y]), self.origin[1] + self.height - 1])
        else:
            raise Exception(f"The direction {direction} is not recognized by the system.")

    def move(self, displacements):
        # Method to change the position, by indicating many displacements in a dict
        opposites = {
            'D': 'U', 'U': 'D', 'R': 'L', 'L': 'R',
            'S': 'N', 'N': 'S', 'E': 'W', 'W': 'E'
        }
        for direction in displacements:
            if displacements[direction] >= 0:
                real_direction, value = direction, displacements[direction]
            else:
                real_direction, value = opposites[direction], - displacements[direction]
            for n in range(value):
                self.one_move(real_direction)

    def get_point(self, position):
        # Method to get the value in the map for a specific set of coordinates [x, y]
        return self.map[position[1] - self.origin[1]][position[0] - self.origin[0]]

    def get_points(self, positions):
        # Method to get the value in the map for multiple points
        return [self.get_point(position) for position in positions]

    def set_point(self, position, marker='#'):
        # Method to change the map on a specific set of coordinates [x, y]
        self.map[position[1] - self.origin[1]][position[0] - self.origin[0]] = marker

    def set_points(self, coordinates, markers='#'):
        # Method to change the map with the same marker (by default '#') on a list of coordinates.
        # If the marker option is set to a list: change the map to the values of the markers list, given in the same
        # order as the coordinates.
        if type(markers) == str:
            for coord in coordinates:
                self.set_point(coord, markers)
        else:
            for n in range(len(coordinates)):
                self.set_point(coordinates[n], markers[n])

    def get_line(self, direction):
        # Method to get the markers of all a line, from the position, in the given direction
        if direction in ['E', 'R']:
            positions = [[v, self.get_position()[1]] for v in range(self.get_position()[0] + 1, self.width)]
        elif direction in ['W', 'L']:
            positions = [[v, self.get_position()[1]] for v in range(self.get_position()[0] - 1, -1, -1)]
        elif direction in ['U', 'N']:
            positions = [[self.get_position()[0], v] for v in range(self.get_position()[1] - 1, -1, -1)]
        elif direction in ['D', 'S']:
            positions = [[self.get_position()[0], v] for v in range(self.get_position()[1] + 1, self.height)]
        else:
            raise Exception("Direction not coded")
        return [self.get_point(pos) for pos in positions]

    def get_line_positions(self, direction):
        # Method to get the coords of all a line, from the position, in the given direction
        if direction in ['E', 'R']:
            positions = [[v, self.get_position()[1]] for v in range(self.get_position()[0] + 1, self.width)]
        elif direction in ['W', 'L']:
            positions = [[v, self.get_position()[1]] for v in range(self.get_position()[0] - 1, -1, -1)]
        elif direction in ['U', 'N']:
            positions = [[self.get_position()[0], v] for v in range(self.get_position()[1] - 1, -1, -1)]
        elif direction in ['D', 'S']:
            positions = [[self.get_position()[0], v] for v in range(self.get_position()[1] + 1, self.height)]
        else:
            raise Exception("Direction not coded")
        return positions

    def get_neighbours(self, diagonals=True):
        # Method to get the values of the map for all the neighbours of the position.
        # Optional: diagonals can be set to False not to get them in the neighbourhood.
        if diagonals:
            return [
                self.map[y - self.origin[1]][x - self.origin[0]]
                for x in range(max([self.origin[0], self.x - 1]), min([self.x + 2, self.width + self.origin[0]]))
                for y in range(max([self.origin[1], self.y - 1]), min([self.y + 2, self.height + self.origin[1]]))
                if [x, y] != [self.x, self.y]
            ]
        else:
            return [
                       self.map[self.y - self.origin[1]][x - self.origin[0]]
                       for x in range(max([self.origin[0], self.x - 1]), min([self.x + 2, self.width + self.origin[0]]))
                       if x != self.x
                   ] + [
                       self.map[y - self.origin[1]][self.x - self.origin[0]]
                       for y in
                       range(max([self.origin[1], self.y - 1]), min([self.y + 2, self.height + self.origin[1]]))
                       if y != self.y
                   ]

    def get_neighbour(self, direction):
        directions = {
            'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0],
            'N': [0, -1], 'S': [0, 1], 'W': [-1, 0], 'E': [1, 0]
        }
        x_moved, y_moved = self.x + directions[direction][0], self.y + directions[direction][1]
        if (min([max([self.origin[0], x_moved]), self.origin[0] + self.width - 1]) != x_moved) | (
                min([max([self.origin[1], y_moved]), self.origin[1] + self.height - 1]) != y_moved):
            return 'Exit'
        return self.map[y_moved][x_moved]

    def get_neighbours_coordinates(self, diagonals=True):
        # Method to get the coordinates for all the neighbours of the position.
        # Optional: diagonals can be set to False not to get them in the neighbourhood.
        if diagonals:
            return [
                [x, y]
                for x in range(max([self.origin[0], self.x - 1]), min([self.x + 2, self.width + self.origin[0]]))
                for y in range(max([self.origin[1], self.y - 1]), min([self.y + 2, self.height + self.origin[1]]))
                if [x, y] != [self.x, self.y]
            ]
        else:
            return [
                       [x, self.y]
                       for x in range(max([self.origin[0], self.x - 1]), min([self.x + 2, self.width + self.origin[0]]))
                       if x != self.x
                   ] + [
                       [self.x, y]
                       for y in
                       range(max([self.origin[1], self.y - 1]), min([self.y + 2, self.height + self.origin[1]]))
                       if y != self.y
                   ]

    def get_neighbourhood_coordinates(self, points, diagonals=False):
        neighbourhood = []
        base = 10 ** (int(np.log10(self.width)) + 1)
        for point in points:
            self.set_position(point)
            neighbourhood = list(set(
                neighbourhood + [base * p[0] + p[1] for p in self.get_neighbours_coordinates(diagonals)]
            ))
        all_points = [[p // base, p % base] for p in neighbourhood]
        return [p for p in all_points if p not in points]

    def count_neighbours(self, marker, diagonals=True):
        # Method to count a specific value of marker in the neighbourhood of the position.
        # Optional: diagonals can be set to False not to get them in the neighbourhood.
        return sum([n == marker for n in self.get_neighbours(diagonals)])

    def count_marker(self, marker):
        # Method to count how many times a specific marker is present in the total map
        return sum([sum([x == marker for x in line]) for line in self.map])

    def change_marker(self, previous_marker, new_marker):
        # Method to update the map to change all the occurrences of a given marker to a new value
        self.map = [[new_marker if point == previous_marker else point for point in line] for line in self.map]

    def apply_function(self, function):
        # Method to update all the values of the points of the map using a given function
        self.map = [[function(point) for point in line] for line in self.map]

    def remove_lines(self, count, top=True):
        if count >= self.height:
            self.map = [[]]
            self.height, self.width = 0, 0
            self.x, self.y = self.origin[0], self.origin[1]
        elif top:
            self.map = self.map[count:]
            self.height -= count
            self.origin = [self.origin[0], self.origin[1] + count]
        else:
            self.map = self.map[:(-count)]
            self.height -= count

    def remove_columns(self, count, left=True):
        if count >= self.width:
            self.map = [[]]
            self.height, self.width = 0, 0
            self.x, self.y = self.origin[0], self.origin[1]
        elif left:
            self.map = [line[count:] for line in self.map]
            self.width -= count
            self.origin = [self.origin[0] + count, self.origin[1]]
        else:
            self.map = [line[:(-count)] for line in self.map]
            self.width -= count

    def add_empty_lines(self, count, top=True):
        if count > 0:
            if top:
                self.map = [['.' for _ in range(self.width)] for _ in range(count)] + self.map
                self.height += count
                self.origin = [self.origin[0], self.origin[1] - count]
            else:
                self.map = self.map + [['.' for _ in range(self.width)] for _ in range(count)]
                self.height += count

    def add_empty_columns(self, count, left=True):
        if count > 0:
            if left:
                self.map = [['.' for _ in range(count)] + line for line in self.map]
                self.width += count
                self.origin = [self.origin[0] - count, self.origin[1]]
            else:
                self.map = [line + ['.' for _ in range(count)] for line in self.map]
                self.width += count

    def create_submap(self, x_min=None, x_max=None, y_min=None, y_max=None):
        # Method to create a new AocMap instance, which represents a part of the given AocMap
        result = self.copy()
        if x_min is not None:
            remove_left = x_min - self.origin[0]
            if remove_left > 0:
                result.remove_columns(remove_left)
        if x_max is not None:
            remove_right = self.origin[0] + self.width - x_max - 1
            if remove_right > 0:
                result.remove_columns(remove_right, left=False)
        if y_min is not None:
            remove_top = y_min - self.origin[1]
            if remove_top > 0:
                result.remove_lines(remove_top)
        if y_max is not None:
            remove_bottom = self.origin[1] + self.height - y_max - 1
            if remove_bottom > 0:
                result.remove_lines(remove_bottom, top=False)
        return result

    def reverse(self, vertical=True, horizontal=False):
        # Method to reverse a map. By default, we turn over the first column and/or the first line of the map. The
        # origin is updated in consequence.
        if vertical:
            for line in self.map:
                line.reverse()
            self.origin = [self.origin[0] - self.width + 1, self.origin[1]]
            self.x = self.width - self.x + self.origin[0]
        if horizontal:
            self.map.reverse()
            self.origin = [self.origin[0], self.origin[1] - self.height + 1]
            self.y = self.height - self.y + self.origin[1]

    def get_marker_coords(self, marker):
        # To get all the coordinates relative to a given marker
        coords = []
        for y in range(self.origin[1], self.origin[1] + self.height):
            for x in range(self.origin[0], self.origin[0] + self.width):
                if self.get_point([x, y]) == marker:
                    coords += [[x, y]]
        return coords

    def superpose(self, by, transparent='.'):
        # Superpose a map by another: the origins of the maps are taken in account to know the overlaps. Empty lines and
        # columns are added if needed. At the end, the resulted map is a larger rectangle. The transparent marker
        # indicates which one is not taken into account in the resulted map.
        self.add_empty_lines(self.origin[1] - by.origin[1], top=True)
        self.add_empty_lines(by.origin[1] - self.origin[1] + by.height - self.height, top=False)
        self.add_empty_columns(self.origin[0] - by.origin[0], left=True)
        self.add_empty_columns(by.origin[0] - self.origin[0] + by.width - self.width, left=False)
        non_transparent = set([x for x in itertools.chain(*by.map) if x != transparent])
        for marker in non_transparent:
            self.set_points(by.get_marker_coords(marker), marker)

    # TODO: write the test
    def glue_map(self, glued, direction='R'):
        # Update the map by adding another one on the right, the left, the top or the bottom
        if (direction in ['R', 'L']) & (glued.height != self.height):
            raise Exception("Cannot glue the map horizontally, its height is not identical to the initial one's.")
        if (direction in ['U', 'D']) & (glued.width != self.width):
            raise Exception("Cannot glue the map vertically, its width is not identical to the initial one's.")
        if direction == 'R':
            self.map = [self.map[y] + glued.map[y] for y in range(self.height)]
            self.width += glued.width
        elif direction == 'L':
            self.map = [glued.map[y] + self.map[y] for y in range(self.height)]
            self.width += glued.width
            self.origin = [self.origin[0] + glued.width, self.origin[1]]
            self.x += glued.x
        elif direction == 'D':
            self.map += glued.map
            self.height += glued.height
        elif direction == 'U':
            self.map = glued.map + self.map
            self.height += glued.height
            self.origin = [self.origin[0], self.origin[1] + glued.height]
            self.y += glued.y
        else:
            raise Exception("The direction must be one of the following: R, L, U, D.")

    def get_paths(self, coords, path=None, end=None):
        if not path:
            path = [coords]
        if end:
            if coords == end:
                return [path]
        self.set_position(coords)
        neighbours = self.get_neighbours_coordinates(diagonals=False)
        accessible_neighbours = [n for n in neighbours if (self.get_point(n) != '#') & (n not in path)]
        if accessible_neighbours:
            paths = []
            for n in accessible_neighbours:
                paths += self.get_paths(n, path + [n], end)
            return paths
        return [path]
