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


import sys

import pygame
from pygame.locals import *

from shared import *

robovacs = []


def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font(SANS_FONT, 18)
    pygame.display.set_caption(ROBOVAC)
    # generate_room()
    while True:
        run_game()


# def generate_room():
    # create_walls() # such that room has odd shape
    # create_dropoffs()
    # create_furniture()
    # create_dogs()
    # create_chargers()
    # create_robovacs()
    # create_dirt()


def run_game():

    while True:  # main game loop

        # robovacs decide

        # move robovacs

        # move dogs

        # update display
        DISPLAY_SURF.fill(BG_COLOR.value)
        draw_grid()
        # draw_walls()
        # draw_dropoffs()
        # draw_furniture()
        # draw_dogs()
        # draw_chargers()
        draw_drawables(robovacs)
        # draw_dirt()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def draw_drawables(drawables):
    for drawable in drawables:
        drawable.draw(DISPLAY_SURF)


def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(DISPLAY_SURF, Colors.DARK_GRAY.value, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAY_SURF, Colors.DARK_GRAY.value, (0, y), (WINDOW_WIDTH, y))


if __name__ == '__main__':
    main()
