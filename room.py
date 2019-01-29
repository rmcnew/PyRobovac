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

from math import fabs

from shared import *
from drawable import Drawable

# room contains methods to create the elements that make up the simulated 
# room where the robovacs operate

# fill a block
def fill_block(block, grid):
    start_x = block[X] * int(GRID_WIDTH / 3)
    stop_x = (block[X] + 1) * int(GRID_WIDTH / 3)
    start_y = block[Y] * int(GRID_HEIGHT / 3)
    stop_y = (block[Y] + 1) * int(GRID_HEIGHT / 3)
    for x in range(start_x, stop_x):
        for y in range(start_y, stop_y):
            grid[x][y] = Drawable.WALL.value


# create the walls
def create_walls(grid):
    # create a border wall so robovacs stay inside the window
    for x in range(0, GRID_WIDTH):
        grid[x][1] = Drawable.WALL.value
        grid[x][GRID_HEIGHT - 1] = Drawable.WALL.value
    for y in range(0, GRID_HEIGHT):
        grid[0][y] = Drawable.WALL.value
        grid[GRID_WIDTH - 1][y] = Drawable.WALL.value
    # randomly generate some wall sections to give the room an unusual shape:
    # 1) divide the room into a 3 x 3 grid
    # 2) randomly choose two blocks and fill them with wall
    first_block = get_random_block()
    #print("first block: {}".format(first_block))
    second_block = get_random_block()
    while (first_block[X] == second_block[X] and first_block[Y] == second_block[Y]) or \
            (fabs(first_block[X] - second_block[X]) == 1 and fabs(first_block[Y] - second_block[Y]) == 1):
        second_block = get_random_block()
    #print("second_block: {}".format(second_block))
    fill_block(first_block, grid)
    fill_block(second_block, grid)

# create the dropoffs
def create_dropoffs():
    dropoffs = []

    return dropoffs

