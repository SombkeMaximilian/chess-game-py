# -*- coding: utf-8 -*-

import pygame as p

def loadImages():
    
    """
    Loads the images of the pieces into memory. A dictionary is used for ease of access.
    """
    
    images = {}
    
    pieces = ["wR", "wN", "wB", "wK", "wQ", "wP", 
              "bR", "bN", "bB", "bK", "bQ", "bP"]
    
    for piece in pieces:
        images[piece] = p.image.load(f"images/pieces/{piece}.png")
        
    results = ["whitewins", "blackwins", "stalemate"]
    
    for result in results:
        images[result] = p.image.load(f"images/endgame/{result}.png")
    
        
    return images
     
   
def drawGameState(window, gamestate, legalMoves, selectedSquare, images, 
                  SQUARE_SIZE, BORDERS, DIM):
    
    """
    Draws a given game state in the window.
    """
    
    # drawing the board itself
    
    boardColors = [p.Color("light gray"), p.Color("dark gray")] 
    
    for row in range(DIM):

        for col in range(DIM):
            
            color = boardColors[((row + col) % 2)]
            square = p.Rect(col*SQUARE_SIZE+BORDERS["l"], row*SQUARE_SIZE+BORDERS["t"], SQUARE_SIZE, SQUARE_SIZE)
            p.draw.rect(window, color, square)
    
    
    # highlighting
    
    highlightMoves(window, gamestate, legalMoves, selectedSquare, SQUARE_SIZE, BORDERS)
    
    
    # drawing the pieces on the board
    
    for row in range(DIM):
        
        for col in range(DIM):
            
            currentSquare = gamestate.board[row, col]
            
            if currentSquare == None:
                continue
            
            square = p.Rect(col*SQUARE_SIZE+BORDERS["l"], row*SQUARE_SIZE+BORDERS["t"], SQUARE_SIZE, SQUARE_SIZE)
            piece = p.transform.scale(images[str(currentSquare)], (SQUARE_SIZE, SQUARE_SIZE))
            window.blit(piece, square)
    
    return


def highlightMoves(window, gamestate, legalMoves, selectedSquare, SQUARE_SIZE, BORDERS):
    
    """
    Highlights selected squares if a turn player's piece is on it and the 
    squares that piece can move to.
    """
    
    # surface for highlighting squares
    highlightedSquare = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
    highlightedSquare.set_alpha(70)
    
    # highlighting last move
    
    if gamestate.moveLog:
        
        lastMove = gamestate.moveLog[-1]
        highlightedSquare.fill(p.Color("yellow"))
        
        moveStart = (lastMove.destinationCol*SQUARE_SIZE+BORDERS["l"], 
                     lastMove.destinationRow*SQUARE_SIZE+BORDERS["t"])
        moveDestination = (lastMove.startCol*SQUARE_SIZE+BORDERS["l"], 
                           lastMove.startRow*SQUARE_SIZE+BORDERS["t"])
        
        window.blit(highlightedSquare, moveStart)
        window.blit(highlightedSquare, moveDestination)
    
    if not selectedSquare:
        return
    
    col, row = selectedSquare
    
    if not gamestate.board.isAlly(row, col, gamestate.turnPlayer):
        return

    # highlighting selected piece
    
    highlightedSquare.fill(p.Color("blue"))
    pieceCoordinates = (col*SQUARE_SIZE+BORDERS["l"], row*SQUARE_SIZE+BORDERS["t"])
    window.blit(highlightedSquare, pieceCoordinates)
    
    # highlighting the piece's possible moves
    
    highlightedSquare.fill(p.Color("green"))
    for move in legalMoves:
        
        if move.startRow == row and move.startCol == col:
            
            moveCoordinates = (move.destinationCol*SQUARE_SIZE+BORDERS["l"], 
                               move.destinationRow*SQUARE_SIZE+BORDERS["t"])
            window.blit(highlightedSquare, moveCoordinates)
    
    return


def drawMoveLog(window, gamestate):
    
    """
    Draws the move log of a game state.
    """
    
    if not gamestate.moveLog:
        return
    
    
    
    return


def drawGameoverText(window, result, images, WIDTH, BORDERS):
    
    """
    Displays the end of game screen when called.
    """
    
    halfBoardX = WIDTH/2 + BORDERS["l"]
    halfBoardY = WIDTH/2 + BORDERS["t"]
    size = (WIDTH * 0.8, WIDTH * 0.4)
    centeredposition = (halfBoardX - size[0]/2, halfBoardY - size[1]/2)
    
    endgamesurface = p.Rect(*centeredposition, *size)
    endgametext = p.transform.scale(images[result], size)
    window.blit(endgametext, endgamesurface)
    
    return