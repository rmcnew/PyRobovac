# PyRobovac, a robotic vacuum AI simulator
# Copyright (C) 2019  Richard Scott McNew.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# A* path finding
from math import fabs
from heapq import *
import json

from direction import Direction
from shared import *


# shared constants and functions
def manhattan_distance(from_location, to_location):
    return fabs(from_location.x - to_location.x) + fabs(from_location.y - to_location.y)


START = None


def get_enterable_adjacent_cells(grid, location):
    cells = []
    for direction in Direction:
        candidate = location.plus(direction)
        if can_enter(grid, candidate):
            cells.append(candidate)
    return cells
        

# extract path 
def extract_path(closed_list, to_location):
    path = []
    node = closed_list[json.dumps(to_location)]
    while node.parent_location != START:
        path.insert(0, node.location)
        node = closed_list[json.dumps(node.parent_location)]
    return path
    

# use A* algorithm to find a path 
def find_path(grid, from_location, to_location):
    nodes = []
    node_index = 0
    open_list = []
    closed_list = {}
    start_node = Node(from_location, 0, manhattan_distance(from_location, to_location), START)
    nodes.append(start_node)
    heappush(open_list, (start_node.cost, node_index))
    node_index = node_index + 1
    while len(open_list) > 0:
        cost, current_node_index = heappop(open_list)
        current_node = nodes[current_node_index]
        closed_list[current_node.location.to_str()] = current_node

        if to_location.to_str() in closed_list:
            path = extract_path(closed_list, to_location)
            print(path)
            return path

        adjacent_cells = get_enterable_adjacent_cells(grid, current_node.location)
        
        for cell in adjacent_cells:
            # print(cell)
            if cell.to_str() in closed_list:
                continue
            if cell not in open_list:
                node_to_add = Node(cell,
                                   current_node.movement_cost + 1,
                                   manhattan_distance(cell, to_location),
                                   current_node.location)
                nodes.append(node_to_add)
                heappush(open_list, (node_to_add.cost, node_index))
                node_index = node_index + 1
    return None


class Node(object):
    def __init__(self, location, movement_cost, heuristic_cost, parent_location):
        self.location = location
        self.movement_cost = movement_cost
        self.heuristic_cost = heuristic_cost
        self.cost = self.movement_cost + self.heuristic_cost
        self.parent_location = parent_location
