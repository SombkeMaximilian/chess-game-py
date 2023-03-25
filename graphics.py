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
     
   
def drawGameState(window, gamestate, legalMoves, selectedSquare, 
                  SQUARE_SIZE, BORDERS, DIM, IMG):
    
    """
    Draws a given game state on screen and updates it.
    """
    
    # drawing the board itself

    boardColors = [p.Color("light gray"), p.Color("dark gray")] 
    
    for row in range(DIM):

        for col in range(DIM):
            
            color = boardColors[((row + col) % 2)]
            square = p.Rect(col*SQUARE_SIZE+BORDERS, row*SQUARE_SIZE+BORDERS, SQUARE_SIZE, SQUARE_SIZE)
            p.draw.rect(window, color, square)
    
    
    # highlighting
    
    highlightMoves(window, gamestate, legalMoves, selectedSquare, SQUARE_SIZE, BORDERS)
    
    
    # drawing the pieces on the board
    
    for row in range(DIM):
        
        for col in range(DIM):
            
            currentSquare = gamestate.board[row, col]
            
            if currentSquare == None:
                continue
            
            square = p.Rect(col*SQUARE_SIZE+BORDERS, row*SQUARE_SIZE+BORDERS, SQUARE_SIZE, SQUARE_SIZE)
            piece = p.transform.scale(IMG[str(currentSquare)], (SQUARE_SIZE, SQUARE_SIZE))
            window.blit(piece, square)
    
    return
            

def highlightMoves(window, gamestate, legalMoves, selectedSquare, SQUARE_SIZE, BORDERS):
    
    """
    Highlights selected squares if a turn player's piece is on it and the 
    squares that piece can move to.
    """
    
    if not selectedSquare:
        return
    
    col, row = selectedSquare
    
    if not gamestate.board.isAlly(row, col, gamestate.turnPlayer):
        return
    
    if gamestate.turnPlayer == gamestate.board[row, col].player:
        
        highlightedSquare = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        highlightedSquare.set_alpha(70)
        highlightedSquare.fill(p.Color("blue"))
        
        pieceCoordinates = (col*SQUARE_SIZE+BORDERS, row*SQUARE_SIZE+BORDERS)
        window.blit(highlightedSquare, pieceCoordinates)
        
        highlightedSquare.fill(p.Color("green"))
        for move in legalMoves:
            
            if move.startRow == row and move.startCol == col:
                
                moveCoordinates = (move.destinationCol*SQUARE_SIZE+BORDERS, 
                                   move.destinationRow*SQUARE_SIZE+BORDERS)
                window.blit(highlightedSquare, moveCoordinates)
    
    return