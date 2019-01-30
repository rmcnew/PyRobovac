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
from robovac import Robovac
from dog import Dog

# room contains methods to create the elements that make up the simulated 
# room where the robovacs operate

# fill a wall block
def fill_wall_block(block, grid):
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
    fill_wall_block(first_block, grid)
    fill_wall_block(second_block, grid)


# fill a dropoff block
def fill_dropoff_block(grid):
    block = get_random_location()
    start_x = block[X]
    start_y = block[Y]
    stop_x = min(block[X] + DROPOFF_SIZE, GRID_WIDTH)
    stop_y = min(block[Y] + DROPOFF_SIZE, GRID_HEIGHT)
    clear = True
    for x in range(start_x, stop_x):
        for y in range(start_y, stop_y):
            if x <= GRID_WIDTH and y <= GRID_HEIGHT and grid[x][y] != Drawable.CLEAN.value:
                clear = False
    if x <= GRID_WIDTH and y <= GRID_HEIGHT and clear:
        for x in range(start_x, stop_x):
            for y in range(start_y, stop_y):
                grid[x][y] = Drawable.DROPOFF.value
    return clear


# create the dropoffs
def create_dropoffs(grid):
    dropoffs_left = DROPOFF_COUNT
    while dropoffs_left > 0:
        if fill_dropoff_block(grid):
            dropoffs_left = dropoffs_left - 1


# fill a furniture block
def fill_furniture_block(grid):
    block = get_random_location()
    start_x = block[X]
    start_y = block[Y]
    stop_x = min(block[X] + FURNITURE_SIZE, GRID_WIDTH)
    stop_y = min(block[Y] + FURNITURE_SIZE, GRID_HEIGHT)
    clear = True
    for x in range(start_x, stop_x):
        for y in range(start_y, stop_y):
            if x <= GRID_WIDTH and y <= GRID_HEIGHT and grid[x][y] != Drawable.CLEAN.value:
                clear = False
    if x <= GRID_WIDTH and y <= GRID_HEIGHT and clear:
        for x in range(start_x, stop_x):
            for y in range(start_y, stop_y):
                grid[x][y] = Drawable.FURNITURE.value
    return clear


# create the furniture
def create_furniture(grid):
    furniture_left = FURNITURE_COUNT
    while furniture_left > 0:
        if fill_furniture_block(grid):
            furniture_left = furniture_left - 1


# create robovacs and chargers
def create_robovacs(grid, count):
    robovacs = []
    robovac_index = 1
    while robovac_index <= count:
        charger_location = get_random_location()
        charger_x = charger_location[X]
        charger_y = charger_location[Y]
        robovac_x = charger_x - 1
        robovac_y = charger_y
        if is_clean(grid, charger_x, charger_y) and is_clean(grid, robovac_x, robovac_y):
            grid[charger_x][charger_y] = Drawable["CHARGER_" + str(robovac_index)].value
            grid[robovac_x][robovac_y] = Drawable["ROBOVAC_" + str(robovac_index)].value
            robovacs.append(Robovac(robovac_x, robovac_y, charger_x, charger_y, "ROBOVAC_" + str(robovac_index)))
            robovac_index = robovac_index + 1
    return robovacs


def create_dogs(grid, count):
    dogs = []
    dog_index = 1
    while dog_index <= count:
        dog_location = get_random_location()
        dog_x = dog_location[X]
        dog_y = dog_location[Y]
        if is_clean(grid, dog_x, dog_y):
            grid[dog_x][dog_y] = Drawable["DOG_" + str(dog_index)].value
            dogs.append(Dog(dog_x, dog_y, "DOG_" + str(dog_index)))
            dog_index = dog_index + 1
    return dogs


def create_dirt(grid):
    dirt = []
    filth = []
    dirt_index = 1
    dirt_count = DIRTY_MIN # TODO: make this semi-random
    while dirt_index <= dirt_count:
        dirt_location = get_random_location()
        dirt_x = dirt_location[X]
        dirt_y = dirt_location[Y]
        if is_clean(grid, dirt_x, dirt_y):
            grid[dirt_x][dirt_y] = Drawable["DIRTY"].value
            dirt.append({X:dirt_x, Y:dirt_y})
            dirt_index = dirt_index + 1
    filth_index = 1
    filth_count = FILTHY_MIN # TODO: make this semi-random
    while filth_index <= filth_count:
        filth_location = get_random_location()
        filth_x = filth_location[X]
        filth_y = filth_location[Y]
        if is_clean(grid, filth_x, filth_y):
            grid[filth_x][filth_y] = Drawable["FILTHY"].value
            filth.append({X:filth_x, Y:filth_y})
            filth_index = filth_index + 1
    return (dirt, filth)
