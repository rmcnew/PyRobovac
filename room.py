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

from shared import *
from wall import Wall

# room contains methods to create the elements that make up the simulated 
# room where the robovacs operate

# create the walls
def create_walls():
    walls = []
    # create a border wall so robovacs stay inside the window
    for x in range(0, GRID_WIDTH):
        walls.append(Wall(x, 1))
        walls.append(Wall(x, GRID_HEIGHT - 1))
    for y in range(0, GRID_HEIGHT):
        walls.append(Wall(0, y))
        walls.append(Wall(GRID_WIDTH - 1, y))
    # randomly generate some wall sections to give the room an unusual shape:
    # 1) divide the room into a 3 x 3 grid
    # 2) randomly choose two blocks and fill them with wall
    first_block = get_random_block()
    print("first block: {}".format(first_block))
    second_block = get_random_block()
    while (first_block[X] == second_block[X] and first_block[Y] == second_block[Y]):
        second_block = get_random_block()
    print("second_block: {}".format(second_block))
    return walls
