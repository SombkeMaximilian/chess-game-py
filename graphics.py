# -*- coding: utf-8 -*-

import pygame as p

def loadPieceImages():
    """
    Loads the images of the pieces into memory. A dictionary is used for ease of access.
    """
    
    images = {}
    
    pieces = ["wR", "wN", "wB", "wK", "wQ", "wP", 
              "bR", "bN", "bB", "bK", "bQ", "bP"]
    
    for piece in pieces:
        images[piece] = p.image.load(f"images/pieces/{piece}.png")
        
    return images
        
def drawGameState(window, gamestate, SQUARE_SIZE: int, DIM: int, IMG: dict):
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