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
from datetime import datetime, timedelta
from shared import *
from drawable import Drawable

class Robovac:
    def __init__(self, start_x, start_y, charger_x, charger_y, name):
        self.x = start_x
        self.y = start_y
        self.charger_x = charger_x
        self.charger_y = charger_y
        self.name = name
        self.direction = RIGHT
        self.battery = BATTERY_FULL
        self.dirty_cleaned = 0
        self.filthy_cleaned = 0
        self.start_time = datetime.now()
        self.action_queue = []
        self.cell_below = Drawable.CLEAN.value

    def score(self, dirty_left, filthy_left):
        elapsed_minutes = (datetime.now() - self.start_time).seconds / SECONDS_PER_MINUTE
        raw_points = (self.dirty_cleaned * DIRTY_CLEANED_SCORE) + (self.filthy_cleaned * FILTHY_CLEANED_SCORE)
        weighted_points = raw_points / elapsed_minutes
        penalty = (dirty_left * DIRTY_MISSED_SCORE) + (filthy_left * FILTHY_MISSED_SCORE)
        return weighted_points + penalty

    def turn_left(self):
        self.battery = self.battery - MOVE_DRAIN
        if self.direction == UP:
            self.direction = LEFT
        elif self.direction == LEFT:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = UP

    def turn_right(self):
        self.battery = self.battery - MOVE_DRAIN
        if self.direction == UP:
            self.direction = RIGHT
        elif self.direction == LEFT:
            self.direction = UP
        elif self.direction == DOWN:
            self.direction = LEFT
        elif self.direction == RIGHT:
            self.direction = DOWN

    def move_forward(self, grid):
        self.battery = self.battery - MOVE_DRAIN
        if self.direction == UP:
            if can_enter(grid, self.x, self.y + 1): # move up
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x][self.y + 1] 
                grid[self.x][self.y + 1] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.y = self.y + 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)
            
        elif self.direction == LEFT:
            if can_enter(grid, self.x - 1, self.y): # move left
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x - 1][self.y] 
                grid[self.x - 1][self.y] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.x = self.x - 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)
            
        elif self.direction == DOWN:
            if can_enter(grid, self.x, self.y - 1): # move down
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x][self.y - 1] 
                grid[self.x][self.y - 1] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.y = self.y - 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)
            
        elif self.direction == RIGHT:
            if can_enter(grid, self.x + 1, self.y): # move right
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x + 1][self.y] 
                grid[self.x + 1][self.y] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.x = self.x + 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)
            
        

    def move_backward(self, grid):
        self.battery = self.battery - MOVE_DRAIN
        if self.direction == DOWN:
            if can_enter(grid, self.x, self.y + 1): # move up
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x][self.y + 1] 
                grid[self.x][self.y + 1] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.y = self.y + 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)
            
        elif self.direction == RIGHT:
            if can_enter(grid, self.x - 1, self.y): # move left
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x - 1][self.y] 
                grid[self.x - 1][self.y] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.x = self.x - 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)
            
        elif self.direction == UP:
            if can_enter(grid, self.x, self.y - 1): # move down
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x][self.y - 1] 
                grid[self.x][self.y - 1] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.y = self.y - 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)
            
        elif self.direction == LEFT:
            if can_enter(grid, self.x + 1, self.y): # move right
                # update the grid for cell below
                previous_cell_below = self.cell_below
                self.cell_below = grid[self.x + 1][self.y] 
                grid[self.x + 1][self.y] = Drawable[self.name].value
                grid[self.x][self.y] = previous_cell_below
                # update internal position
                self.x = self.x + 1
            else: # cannot move up, back off and change direction
                self.action_queue.insert(0, TURN_LEFT)


    def vacuum(self):
        self.battery = self.battery - VACUUM_DRAIN
        if self.cell_below == Drawable.FILTHY.value:
            self.cell_below = Drawable.DIRTY.value
            self.filthy_cleaned = self.filthy_cleaned + 1
        elif self.cell_below == Drawable.DIRTY.value:
            self.cell_below = Drawable.CLEAN.value
            self.dirty_cleaned = self.dirty_cleaned + 1
