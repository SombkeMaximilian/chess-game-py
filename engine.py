# -*- coding: utf-8 -*-

class GameState():
    
    """
    This class stores all the information about the game state. Legal moves, the board, a log of 
    moves, whose turn it is, etc.
    """
    
    def __init__(self):
        
        """
        Board is a 2-dimensional list, each element represents a square on a 
        chess board and it has 8 rows and 8 columns. 
        The players are:
        b = black
        w = white
        Using standard chess notation for the pieces:
        R = rook
        N = knight
        B = bishop
        Q = queen
        K = king
        P = pawn
        Squares that have no piece are represented by em (empty).
        """
        
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["em", "em", "em", "em", "em", "em", "em", "em"],
            ["em", "em", "em", "em", "em", "em", "em", "em"],
            ["em", "em", "em", "em", "em", "em", "em", "em"],
            ["em", "em", "em", "em", "em", "em", "em", "em"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        
        self.players = ["white", "black"]
        self.turnPlayer = "white"
        self.moveLog = []
        
        
        
    def performMove(self, MovePiece):
        """
        Alters the board to reflect a performed move and changes turn player.
        """
        
        self.board[MovePiece.startRow][MovePiece.startCol] = "em"
        self.board[MovePiece.destinationRow][MovePiece.destinationCol] = MovePiece.movedPiece
        
        self.moveLog.append(MovePiece)
        self.turnPlayer = [player for player in self.players 
                           if player != self.turnPlayer][0]
        
class MovePiece():
    """
    This class is responsible for calculating moves of pieces, it also stores
    the information about which piece was moved and which piece was captured,
    if any.
    """
    
    
    def __init__(self, start: tuple, destination: tuple, board):
        
        # store start position and destination
        self.startRow, self.startCol = start
        self.destinationRow, self.destinationCol = destination
        
        # store moved and captured pieces
        self.movedPiece = board[self.startRow][self.startCol]
        self.capturedPiece = board[self.destinationRow][self.destinationCol]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        