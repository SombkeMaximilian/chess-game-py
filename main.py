# -*- coding: utf-8 -*-

import pygame as p
import math

import engine
import graphics


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
    
    # list that will store the legal moves
    legalMoves = gamestate.generateLegalMoves()
    
    # flag for when a move was made to avoid generating legal moves every frame
    newGameState = False
    
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
                    
                    # save coordinates of the click
                    selectedSquare = mouseClick
                    moveCoordinates.append(reversed(selectedSquare))
                
                # move piece if 2 clicks in different squares were made
                if len(moveCoordinates) == 2:
                    
                    # generate a move object with the inputs
                    move = engine.Move(*moveCoordinates, gamestate.board)
                    
                    # check of the move complies with the rules
                    if move in legalMoves: 
                        
                        # perform the move
                        gamestate.performMove(move)
                        
                        # set flag to true to generate new legal moves
                        newGameState = True
                                                
                    # unselected everything again
                    selectedSquare = ()
                    moveCoordinates = []
        
            # key presses
            if event.type == p.KEYDOWN:
                
                # u is the hotkey
                if event.key == p.K_u:
                    
                    # undo the move
                    gamestate.undoMove()
                    
                    # set flag to true to generate legal moves again
                    newGameState = True
        
        # check if the game state has changed
        if newGameState == True:
            
            # generate new set of legal moves
            legalMoves = gamestate.generateLegalMoves()
            
            # set flag back to false
            newGameState = False
            
        # update the graphics
        graphics.drawGameState(window, gamestate, SQUARE_SIZE, BORDERS, DIM, IMG)
    
        clock.tick(FPS)
        p.display.flip()
    
    # close the window
    p.quit()
    
    
if __name__ == "__main__":
    
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
    BORDERS = 100
    DIM = 8
    SQUARE_SIZE = int(WIDTH / DIM)
    FPS = 30
    IMG = {}
    
    main()