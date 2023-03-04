# -*- coding: utf-8 -*-

import pygame as p
import math

import engine
import graphics

"""
Global variables for displaying the chess board.
WIDTH and HEIGHT of the board, possibly allow the user to change this later.
BORDERS around the board for extra features.
DIM = Dimensions of the board is always 8.
Each row and column has 8 squares of size SQUARE_SIZE.
FPS the game runs at, possibly allow the user to change this later.
Image names of the pieces will be kept in the dictionary IMG.
"""

WIDTH = HEIGHT = 512
BORDERS = 200
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
    window = p.display.set_mode((WIDTH+2*BORDERS, HEIGHT+2*BORDERS))
    window.fill(p.Color("white"))
    # get a pygame clock
    clock = p.time.Clock()
    
    # generate a GameState object
    gamestate = engine.GameState()
    
    # load the pieces into memory
    IMG = graphics.loadPieceImages()
    
    # keeping track of mouse clicks and which piece is being moved
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
            
            # mouse presses
            if event.type == p.MOUSEBUTTONDOWN:
                
                # read coordinates of mouse clicks 
                mouseClick = tuple(math.floor((coordinate - BORDERS) / SQUARE_SIZE) 
                                   for coordinate in p.mouse.get_pos())
                
                # unselecting by clicking again
                if mouseClick == selectedSquare:
                    
                    selectedSquare = ()
                    moveCoordinates = []
                
                # check if click is inside the chess board
                elif mouseClick[0] in range(8) and mouseClick[1] in range(8):
                    
                    selectedSquare = mouseClick
                    moveCoordinates.append(reversed(selectedSquare))
                
                # move piece if 2 clicks in different squares were made
                if len(moveCoordinates) == 2:
                    
                    move = engine.Move(moveCoordinates[0], moveCoordinates[1], gamestate.board)
                    gamestate.performMove(move)
                    
                    selectedSquare = ()
                    moveCoordinates = []
        
            # key presses
            if event.type == p.KEYDOWN:
                
                # undo moves
                if event.key == p.K_u:
                    gamestate.undoMove()
                                
        
        # update the graphics
        graphics.drawGameState(window, gamestate, SQUARE_SIZE, BORDERS, DIM, IMG)
    
        clock.tick(FPS)
        p.display.flip()
    
    # close the window
    p.quit()
    
    
if __name__ == "__main__":
    main()