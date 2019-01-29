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

# frames per second
FPS = 15

# game window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960

# cell size and game grid
CELL_SIZE = 10
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
GRID_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
GRID_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

# background color
BG_COLOR = Colors.BLACK

# game title
ROBOVAC = 'Robovac'

# game font
SANS_FONT = 'freesansbold.ttf'

# coordinates
X = 'x'
Y = 'y'

# cardinal directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# robovac vacuum
VACUUM_CLEAN = 1

# robovac battery
BATTERY_FULL = 300
MOVE_DRAIN = 1
VACUUM_DRAIN = 2



def get_random_location():
    return {X: random.randint(0, GRID_WIDTH - 1), Y: random.randint(0, GRID_HEIGHT - 1)}

def get_random_block():
    return {X: random.randint(0, 2), Y: random.randint(0, 2)}
