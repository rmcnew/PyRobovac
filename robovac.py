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

# robovac module
from datetime import datetime

from direction import Direction
from shared import *


class Robovac:
    def __init__(self, start_location, charger_location, name):
        self.location = start_location
        self.charger_location = charger_location
        self.name = Drawable[name]
        self.direction = Direction.EAST
        self.battery = BATTERY_FULL
        self.dirty_cleaned = 0
        self.filthy_cleaned = 0
        self.start_time = datetime.now()
        self.action_queue = []
        self.cell_below = Drawable.CLEAN

    def score(self, dirty_left, filthy_left):
        elapsed_minutes = (datetime.now() - self.start_time).seconds / SECONDS_PER_MINUTE
        raw_points = (self.dirty_cleaned * DIRTY_CLEANED_SCORE) + (self.filthy_cleaned * FILTHY_CLEANED_SCORE)
        weighted_points = raw_points / elapsed_minutes
        penalty = (dirty_left * DIRTY_MISSED_SCORE) + (filthy_left * FILTHY_MISSED_SCORE)
        return weighted_points + penalty

    def turn_north(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.NORTH

    def turn_northeast(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.NORTHEAST

    def turn_east(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.EAST

    def turn_southeast(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.SOUTHEAST

    def turn_south(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.SOUTH

    def turn_southwest(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.SOUTHWEST

    def turn_west(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.WEST

    def turn_northwest(self):
        self.battery = self.battery - MOVE_DRAIN
        self.direction = Direction.NORTHWEST

    def move_forward(self, grid):
        self.battery = self.battery - MOVE_DRAIN
        next_location = self.location.plus(self.direction)
        if can_enter(grid, next_location):
            # save the cell below for the next location
            next_cell_below = grid[next_location]
            # put the current cell below back on the grid
            grid[self.location] = self.cell_below
            # update the grid for the robovac's next location
            grid[next_location] = self.name
            # set the cell below to the next location
            self.cell_below = next_cell_below
            # update internal location
            self.location = next_location
        else:  # cannot move up, back off and change direction
            self.action_queue.insert(0, TURN_LEFT)

    def move_backward(self, grid):
        self.battery = self.battery - MOVE_DRAIN
        next_location = self.location.minus(self.direction)
        if can_enter(grid, next_location):
            # save the cell below for the next location
            next_cell_below = grid[next_location]
            # put the current cell below back on the grid
            grid[self.location] = self.cell_below
            # update the grid for the robovac's next location
            grid[next_location] = self.name
            # set the cell below to the next location
            self.cell_below = next_cell_below
            # update internal location
            self.location = next_location
        else:  # cannot move up, back off and change direction
            self.action_queue.insert(0, TURN_LEFT)

    def vacuum(self):
        self.battery = self.battery - VACUUM_DRAIN
        if self.cell_below == Drawable.FILTHY.value:
            self.cell_below = Drawable.DIRTY.value
            self.filthy_cleaned = self.filthy_cleaned + 1
        elif self.cell_below == Drawable.DIRTY.value:
            self.cell_below = Drawable.CLEAN.value
            self.dirty_cleaned = self.dirty_cleaned + 1
