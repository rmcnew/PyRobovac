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

# drawable, a base class for drawable point objects

from shared import *
import pygame
from pygame.locals import *


class Drawable:
    def __init__(self, x, y, line_color, fill_color):
        self.x = x
        self.y = y
        self.lineColor = line_color
        self.fillColor = fill_color

    def draw(self, DISPLAY_SURF):
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, self.lineColor.value, rect)
        inner_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(DISPLAY_SURF, self.fillColor.value, inner_rect)
