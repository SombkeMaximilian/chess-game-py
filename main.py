# -*- coding: utf-8 -*-

"""
Main driver file. Handles inputs and displaying the game state on screen.
"""

import pygame as p
import engine

"""
Global variables for displaying the chess board.
WIDTH and HEIGHT of the board, possibly allow the user to change this later.
DIM = Dimensions of the board is always 8.
Each row and column has 8 squares of size SQUARE_SIZE.
FPS the game runs at, possibly allow the user to change this later.
Image names of the pieces will be kept in the dictionary IMG.
"""

WIDTH = HEIGHT = 1024
DIM = 8
SQUARE_SIZE = WIDTH / DIM
FPS = 10
IMG = {}

p.init()