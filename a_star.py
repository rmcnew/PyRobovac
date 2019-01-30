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
from shared import *


# shared constants and functions
def manhattan_distance(x1, y1, x2, y2):
    return fabs(x1 - x2) + fabs(y1 - y2)


START = None


def get_adjacent_cells(grid, x, y):
    cells = []
    if can_enter(grid, x+1, y):
        cells.append({X: x+1, Y: y})
    if can_enter(grid, x, y+1):
        cells.append({X: x, Y: y+1})
    if can_enter(grid, x-1, y):
        cells.append({X: x-1, Y: y})
    if can_enter(grid, x, y-1):
        cells.append({X: x, Y: y-1})
    return cells
        

# extract path 
def extract_path(closed_list, to_x, to_y):
    path = []
    node = closed_list[json.dumps({X: to_x, Y: to_y})]
    while node.parent_x != START:
        path.insert(0, {X: node.x, Y: node.y})
        node = closed_list[json.dumps({X: node.parent_x, Y: node.parent_y})]
    return path
    

# use A* algorithm to find a path 
def find_path(grid, from_x, from_y, to_x, to_y):
    open_list = []
    closed_list = {}
    start_node = Node(from_x, from_y, 0, manhattan_distance(from_x, from_y, to_x, to_y), START, START)
    heappush(open_list, (start_node.cost(), json.dumps(start_node.__dict__)))
    while len(open_list) > 0:
        (cost, current_node_str) = heappop(open_list)
        # print(current_node_str)
        current_node = json.loads(current_node_str)
        closed_list[json.dumps({X:current_node[X], Y:current_node[Y]})] = current_node

        if json.dumps({X:to_x, Y:to_y}) in closed_list:
            path = extract_path(closed_list, to_x, to_y)  
            print(path)
            return path

        adjacent_cells = get_adjacent_cells(grid, current_node[X], current_node[Y])
        
        for cell in adjacent_cells:
            # print(cell)
            if json.dumps(cell) in closed_list:
                continue
            if cell not in open_list:
                node_to_add = Node(cell[X], cell[Y], int(current_node["movement_cost"]) + 1, manhattan_distance(cell[X], cell[X], to_x, to_y), current_node[X], current_node[Y])
                heappush(open_list, (node_to_add.cost(), json.dumps(node_to_add.__dict__)))
    return None


class Node(object):
    def __init__(self, x, y, movement_cost, heuristic_cost, parent_x, parent_y):
        self.x = x
        self.y = y
        self.movement_cost = movement_cost
        self.heuristic_cost = heuristic_cost
        self.parent_x = parent_x
        self.parent_y = parent_y

    def cost(self):
        return self.movement_cost + self.heuristic_cost
