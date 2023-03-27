# -*- coding: utf-8 -*-

import pygame as p
import itertools

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
    
    images["frame"] = p.image.load("images/frame.png")
    
    return images
     
   
def drawGameState(window, gamestate, legalMoves, selectedSquare, images, font,
                  totalWidth, totalHeight, HEIGHT, SQUARE_SIZE, BORDERS, DIM):
    
    """
    Draws a given game state in the window.
    """
    
    # frame around the board
    
    frameRect = p.Rect(0, 0, totalWidth, totalHeight)
    frame = images["frame"]
    window.blit(frame, frameRect)
    
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
            
    # drawing the move log
    
    drawMoveLog(window, gamestate, font, totalWidth, HEIGHT, BORDERS)
        
    return


def highlightMoves(window, gamestate, legalMoves, selectedSquare, SQUARE_SIZE, BORDERS):
    
    """
    Highlights selected squares if a turn player's piece is on it and the 
    squares that piece can move to.
    """
    
    # surface for highlighting squares
    highlightedSquare = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
    highlightedSquare.set_alpha(70)
    
    # highlighting the king if it's in check
    
    if gamestate.kings[gamestate.turnPlayer].inCheck:
        
        highlightedSquare.fill(p.Color("red"))
        king = gamestate.kings[gamestate.turnPlayer]
        
        kingCoordinates = (king.col*SQUARE_SIZE+BORDERS["l"], 
                           king.row*SQUARE_SIZE+BORDERS["t"])
        window.blit(highlightedSquare, kingCoordinates)
    
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


def drawMoveLog(window, gamestate, font, totalWidth, HEIGHT, BORDERS):
    
    """
    Draws the move log of a game state.
    """
    
    moveLogX = totalWidth-BORDERS["r"] + 25
    moveLogY = BORDERS["t"]
    moveLogWidth = BORDERS["r"] - 50
    moveLogHeight = HEIGHT
    
    # erase previous move log
    logRect = p.Rect(moveLogX, moveLogY, moveLogWidth, moveLogHeight)
    window.fill(p.Color("white"), logRect)
    
    if not gamestate.moveLog:
        return
    
    gap = 14
    
    logText = []
    
    # convert the move log to strings of turns
    for i in range(0, len(gamestate.moveLog), 2):
        
        turn = str(i//2 + 1) + ". " + str(gamestate.moveLog[i]) + " "
        
        if i+1 < len(gamestate.moveLog):
            
            turn += str(gamestate.moveLog[i+1]) + " "
        
        logText.append(turn)
    
    # taken from https://docs.python.org/3/library/itertools.html#itertools-recipes
    def grouper(iterable, n, *, incomplete='fill', fillvalue=" "):
        
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)
    
    turnsPerLine = 3
    currLine = 0
    
    for line in grouper(logText, turnsPerLine):
        
        text = font.render("".join(line), True, p.Color("black"))
        textBox = p.Rect(moveLogX, moveLogY+currLine*gap, moveLogWidth, gap)
        window.blit(text, textBox)
        currLine += 1
        
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