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

from action import Action
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

    def run(self, grid):  # take a turn
        if len(self.action_queue) > 0:
            action = self.action_queue.pop(0)
            self.do_action(action, grid)
        # put decision logic here
        self.move_backward(grid)

    def do_action(self, action, grid):
        if action is Action.MOVE_FORWARD or action is Action.MOVE_BACKWARD:
            getattr(self, action.value)(grid)
        else:
            getattr(self, action.value)()

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

    def turn_left(self):
        self.battery = self.battery - MOVE_DRAIN
        if self.direction is Direction.NORTH:
            self.direction = Direction.WEST
        elif self.direction is Direction.NORTHEAST:
            self.direction = Direction.NORTHWEST
        elif self.direction is Direction.EAST:
            self.direction = Direction.NORTH
        elif self.direction is Direction.SOUTHEAST:
            self.direction = Direction.NORTHEAST
        elif self.direction is Direction.SOUTH:
            self.direction = Direction.EAST
        elif self.direction is Direction.SOUTHWEST:
            self.direction = Direction.SOUTHEAST
        elif self.direction is Direction.WEST:
            self.direction = Direction.SOUTH
        elif self.direction is Direction.NORTHWEST:
            self.direction = Direction.SOUTHWEST

    def turn_right(self):
        self.battery = self.battery - MOVE_DRAIN
        if self.direction is Direction.NORTH:
            self.direction = Direction.EAST
        elif self.direction is Direction.NORTHEAST:
            self.direction = Direction.SOUTHEAST
        elif self.direction is Direction.EAST:
            self.direction = Direction.SOUTH
        elif self.direction is Direction.SOUTHEAST:
            self.direction = Direction.SOUTHWEST
        elif self.direction is Direction.SOUTH:
            self.direction = Direction.WEST
        elif self.direction is Direction.SOUTHWEST:
            self.direction = Direction.NORTHWEST
        elif self.direction is Direction.WEST:
            self.direction = Direction.NORTH
        elif self.direction is Direction.NORTHWEST:
            self.direction = Direction.NORTHEAST

    def move_forward(self, grid):
        self.battery = self.battery - MOVE_DRAIN
        next_location = self.location.plus(self.direction)
        if can_enter(grid, next_location):
            grid.enter(next_location, self.name)
            grid.exit(self.location, self.name)
            # update internal location
            self.location = next_location
        else:  # cannot move up, back off and change direction
            self.action_queue.insert(0, Action.TURN_LEFT)

    def move_backward(self, grid):
        self.battery = self.battery - MOVE_DRAIN
        next_location = self.location.minus(self.direction)
        if can_enter(grid, next_location):
            # print("{}: Exiting {}, Entering {}".format(self.name, self.location, next_location))
            # print("Before Grid: current location: {}, next location: {}".format(grid[self.location], grid[next_location]))
            grid.enter(next_location, self.name)
            grid.exit(self.location, self.name)
            # print("After Grid: current location: {}, next location: {}".format(grid[self.location], grid[next_location]))
            # update internal location
            self.location = next_location
        else:  # cannot move up, back off and change direction
            self.action_queue.insert(0, Action.TURN_LEFT)

    def vacuum(self, grid):
        self.battery = self.battery - VACUUM_DRAIN
        if grid[self.location] is Drawable["{}_AND_FILTHY".format(self.name)]:
            grid[self.location] = Drawable["{}_AND_DIRTY".format(self.name)]
            self.filthy_cleaned = self.filthy_cleaned + 1
        elif grid[self.location] is Drawable["{}_AND_DIRTY".format(self.name)]:
            grid[self.location] = Drawable[self.name]
            self.dirty_cleaned = self.dirty_cleaned + 1
