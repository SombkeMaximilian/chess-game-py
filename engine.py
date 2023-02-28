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