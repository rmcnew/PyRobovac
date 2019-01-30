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
import argparse

import numpy
import pygame
from pygame.locals import *

from shared import *
from drawable import Drawable
import room
from a_star import *

# setup command line argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-r', default=1, type=int, choices=range(1, 5), help='number of robovacs (1 to 4)')
parser.add_argument('-d', default=1, type=int, choices=range(0, 5), help='number of dogs (0 to 4)')
args = parser.parse_args()

# create grid 
grid = numpy.zeros((GRID_WIDTH, GRID_HEIGHT), numpy.int8)
# generate room
room.create_walls(grid) # such that room has odd shape
room.create_dropoffs(grid)
room.create_furniture(grid)
robovacs = room.create_robovacs(grid, args.r)
dogs = room.create_dogs(grid, args.d)
(dirt, filth) = room.create_dirt(grid)


def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font(SANS_FONT, 18)
    pygame.display.set_caption(ROBOVAC)
    # find_path(grid, robovacs[0].x, robovacs[0].y, 0, 0)
    run_game()


def check_for_quit():
    for event in pygame.event.get():  # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE):
            terminate()

def run_game():
    while True:  # main game loop
        # check for q or Esc keypress or window close events to quit
        check_for_quit()
        # robovacs decide

        # move robovacs

        # move dogs

        # update display
        DISPLAY_SURF.fill(BG_COLOR.value)
        draw_grid()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def draw_grid():
    # draw gridlines
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(DISPLAY_SURF, Colors.DARK_GRAY.value, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAY_SURF, Colors.DARK_GRAY.value, (0, y), (WINDOW_WIDTH, y))
    # draw grid objects
    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            if grid[x][y] != 0:
                (lineColor, fillColor) = Drawable(grid[x][y]).color
                cell_x = x * CELL_SIZE
                cell_y = y * CELL_SIZE
                rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(DISPLAY_SURF, lineColor.value, rect)
                inner_rect = pygame.Rect(cell_x + 4, cell_y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
                pygame.draw.rect(DISPLAY_SURF, fillColor.value, inner_rect)

if __name__ == '__main__':
    main()
