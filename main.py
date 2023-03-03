# -*- coding: utf-8 -*-

import pygame as p
import math

import engine
import graphics

"""
Global variables for displaying the chess board.
WIDTH and HEIGHT of the board, possibly allow the user to change this later.
DIM = Dimensions of the board is always 8.
Each row and column has 8 squares of size SQUARE_SIZE.
FPS the game runs at, possibly allow the user to change this later.
Image names of the pieces will be kept in the dictionary IMG.
"""

WIDTH = HEIGHT = 512
DIM = 8
SQUARE_SIZE = int(WIDTH / DIM)
FPS = 10
IMG = {}


def main():
    """
    Handles inputs and updating the game state on screen.
    """
    
    #initialize pygame
    p.init()
    
    # get a pygame window
    window = p.display.set_mode((WIDTH, HEIGHT))
    # get a pygame clock
    clock = p.time.Clock()
    
    # generate a GameState object
    gamestate = engine.GameState()
    
    # load the pieces into memory
    IMG = graphics.loadPieceImages()
    
    # keeping track of mouse clicks and which piece is being moved
    clicks = 0
    selectedSquare = ()
    moveCoordinates = []
    
    # start running the game, this section updates game state and graphics
    active = True
    while active:
        
        # event queue
        for event in p.event.get():
            
            # stop the while loop if the user exits the game
            if event.type == p.QUIT:
                
                active = False
            
            if event.type == p.MOUSEBUTTONDOWN:
                
                # read coordinates of mouse clicks 
                mouseClick = (math.floor(coordinate / SQUARE_SIZE) 
                              for coordinate in p.mouse.get_pos())
                
                # unselecting the square
                if mouseClick == selectedSquare:
                    
                    selectedSquare = ()
                    moveCoordinates = []
                    clicks = 0
                
                # store coordinates of the mouse click
                else:
                    
                    selectedSquare = mouseClick
                    moveCoordinates.append(selectedSquare)
                    clicks += 1
                
                if clicks == 2:
                    
                    pass
                    
        
        # update the graphics
        graphics.drawGameState(window, gamestate, SQUARE_SIZE, DIM, IMG)
    
        clock.tick(FPS)
        p.display.flip()
    
    # close the window
    p.quit()
    
    
if __name__ == "__main__":
    main()