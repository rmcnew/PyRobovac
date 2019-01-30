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

# dog module
import random

from shared import *
from direction import Direction


class Dog:
    def __init__(self, start_location, name):
        self.location = start_location
        self.name = Drawable[name]
        self.direction = Direction.NORTH
        self.dirt_counter = 0

    def turn_north(self):
        self.direction = Direction.NORTH

    def turn_northeast(self):
        self.direction = Direction.NORTHEAST

    def turn_east(self):
        self.direction = Direction.EAST

    def turn_southeast(self):
        self.direction = Direction.SOUTHEAST

    def turn_south(self):
        self.direction = Direction.SOUTH

    def turn_southwest(self):
        self.direction = Direction.SOUTHWEST

    def turn_west(self):
        self.direction = Direction.WEST

    def turn_northwest(self):
        self.direction = Direction.NORTHWEST

    def turn_random(self):
        index = random.randint(0, 7)
        current_index = 0
        for direction in Direction:
            if current_index == index:
                getattr(self, "turn_{}".format(direction.name.lower()))()
            current_index = current_index + 1

    def move_forward(self, grid):
        next_location = self.location.plus(self.direction)
        if can_enter(grid, next_location):
            grid.enter(next_location, self.name)
            grid.exit(self.location, self.name)
            # update internal location
            self.location = next_location

    def run(self, grid):
        if random.randint(1, 100) > 60:
            self.turn_random()
            self.move_forward(grid)
            # if the floor is filthy, increment dirt counter
            if grid[self.location].name.endswith('FILTHY') and random.randint(1, 100) > 75:
                self.dirt_counter = self.dirt_counter + 1
            # if the floor is clean and the dog is dirty, make the floor dirty
            elif not (grid[self.location].name.endswith('FILTHY')) and \
                    not (grid[self.location].name.endswith('DIRTY')) and self.dirt_counter > 0:
                grid[self.location] = Drawable["{}_AND_DIRTY".format(self.name.name)]
                self.dirt_counter = self.dirt_counter - 1
