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
from drawable import Drawable
from shared import *

class Robovac:
    def __init__(self, start_x, start_y, charger_x, charger_y, name):
        self.x = start_x
        self.y = start_y
        self.charger_x = charger_x
        self.charger_y = charger_y
        self.name = name
        self.direction = RIGHT
