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


# shared constants and functions
import random
from colors import Colors
from drawable import Drawable

# frames per second
from point import Point

FPS = 30

# game window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960

# cell size and game grid
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."

# background color
BG_COLOR = Colors.BLACK

# game title
ROBOVAC = 'Robovac'

# game font
SANS_FONT = 'freesansbold.ttf'

# coordinates
X = 'x'
Y = 'y'

# robovac vacuum
VACUUM_CLEAN = 1

# robovac battery
BATTERY_FULL = 1000
BATTERY_LOW = 300
MOVE_DRAIN = 1
VACUUM_DRAIN = 2
BATTERY_CHARGE = 50

# dropoff
DROPOFF_SIZE = 3
DROPOFF_COUNT = 3

# furniture
FURNITURE_SIZE = 4
FURNITURE_COUNT = 7 

# score
DIRTY_CLEANED_SCORE = 10
FILTHY_CLEANED_SCORE = 20
DIRTY_MISSED_SCORE = -1
FILTHY_MISSED_SCORE = -2
SECONDS_PER_MINUTE = 60

# dirt
DIRTY_MIN = 400
FILTHY_MIN = 120

# dirt seeking
NO_DIRT_MAX = 11


def get_random_location(grid):
    return Point(random.randint(0, grid.width - 1), random.randint(0, grid.height - 1))


def get_random_block():
    return Point(random.randint(0, 2), random.randint(0, 2))


def on_grid(grid, point):
    return 0 <= point.x <= grid.width and 0 <= point.y <= grid.height


def is_clean(grid, point):
    return on_grid(grid, point) and grid.array[point.x][point.y] == Drawable.CLEAN.value


def is_dirty(grid, point):
    return on_grid(grid, point) and grid.array[point.x][point.y] == Drawable.DIRTY.value


def is_filthy(grid, point):
    return on_grid(grid, point) and grid.array[point.x][point.y] == Drawable.FILTHY.value


def can_enter(grid, point):
    return on_grid(grid, point) and \
           (grid.array[point.x][point.y] == Drawable.CLEAN.value or
            grid.array[point.x][point.y] == Drawable.DIRTY.value or
            grid.array[point.x][point.y] == Drawable.FILTHY.value)
