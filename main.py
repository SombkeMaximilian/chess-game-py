# -*- coding: utf-8 -*-

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
SQUARE_SIZE = int(WIDTH / DIM)
FPS = 10
IMG = {}

def loadPieceImages():
    """
    Loads the images of the pieces into memory. A dictionary is used for ease of access.
    """
    
    pieces = ["wR", "wN", "wB", "wK", "wQ", "wP", 
              "bR", "bN", "bB", "bK", "bQ", "bP"]
    
    for piece in pieces:
        IMG[piece] = p.image.load(f"images/pieces/{piece}.png")
        
def drawGameState(window, gamestate):
    """
    Draws a given game state on screen and updates it.
    """
    
    # drawing the board itself
    
    boardColors = [p.Color("light gray"), p.Color("dark gray")] 
    
    for row in range(DIM):

        for col in range(DIM):
            
            # color that the square should have, even indices are white, odd are black
            color = boardColors[((row + col) % 2)]
            # rect object with x, y position of square and its size
            square = p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            # draw the rectangle
            p.draw.rect(window, color, square)
    
    
    # drawing the pieces on the board
    
    for row in range(DIM):
        
        for col in range(DIM):
            
            # the piece on the squares are stored as a list of rows
            currentSquare = gamestate.board[row][col]
            
            # skip to the next iteration if the current square is supposed to be empty
            if currentSquare == "em":
                continue
            
            square = p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            piece = p.transform.scale(IMG[currentSquare], (SQUARE_SIZE, SQUARE_SIZE))
            window.blit(piece, square)
            
    
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
    loadPieceImages()
    
    # start running the game, this section updates game state and graphics
    active = True
    while active:
        
        # event queue
        for event in p.event.get():
            
            # stop the while loop if the user exits the game
            if event.type == p.QUIT:
                active = False
        
        # update the graphics
        drawGameState(window, gamestate)
    
        clock.tick(FPS)
        p.display.flip()
    
    # close the window
    p.quit()
    
    
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    