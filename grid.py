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
import numpy
from shared import WINDOW_HEIGHT, WINDOW_WIDTH, CELL_SIZE
from drawable import Drawable


class Grid:
    def __init__(self):
        self.width = int(WINDOW_WIDTH / CELL_SIZE)
        self.height = int(WINDOW_HEIGHT / CELL_SIZE)
        # create grid
        self.array = numpy.zeros((self.width, self.height), numpy.int8)

    def __getitem__(self, item):  # item must be a Point
        return Drawable(self.array[item.x][item.y])

    def __setitem__(self, key, value):  # key must be a Point, value must be a Drawable
        self.array[key.x][key.y] = value.value
