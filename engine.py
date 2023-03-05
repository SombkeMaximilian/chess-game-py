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
        self.players = ["w", "b"]
        self.turnPlayer = "w"
        self.moveLog = []
        
        
    def performMove(self, Move):
        """
        Alters the board to reflect a performed move and changes turn player.
        """
        
        # move the piece on the board
        self.board[Move.startRow][Move.startCol] = "em"
        self.board[Move.destinationRow][Move.destinationCol] = Move.movedPiece
        
        # add the move to the log
        self.moveLog.append(Move)
        
        # change the turn player
        self.turnPlayer = [player for player in self.players 
                           if player != self.turnPlayer][0]
        
    
    def undoMove(self):
        """
        Undo the last move.
        """
        
        # check if there is a move to undo (log is not empty)
        if self.moveLog:
            
            # grab the last move and remove it from the log
            lastMove = self.moveLog[-1]    
            del self.moveLog[-1]
            
            # undo the move
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.movedPiece
            self.board[lastMove.destinationRow][lastMove.destinationCol] = lastMove.capturedPiece
            
            # change the turn player back
            self.turnPlayer = [player for player in self.players 
                               if player != self.turnPlayer][0]
    
    def generateLegalMoves(self):
        """
        Filter out the moves that cannot be made, for example because a move
        would leave the turn player in check afterwards.
        """
        return self.generateAllMoves()
    
    
    def generateAllMoves(self):
        """
        Generates all possible moves for the turn player.
        """
        
        # list that contains the moves
        moves = [Move((7,6), (5,5), self.board)]
        
        # dictionary for calling the corresponding function
        pieceMoveLogic = {"P" : self.pawnMoveLogic,
                          "R" : self.rookMoveLogic,
                          "N" : self.knightMoveLogic,
                          "B" : self.bishopMoveLogic,
                          "Q" : self.queenMoveLogic,
                          "K" : self.kingMoveLogic
                          }
                
        # iterate over all squares on the board
        for row in range(8):
            
            for col in range(8):
                
                # grab the information about what is on the current square
                piece = self.board[row][col]
                
                # check if piece belongs to the turn player (w or b)
                if piece[0] == self.turnPlayer:
                    
                    # generate available moves for the type of piece
                    pieceMoveLogic[piece[1]](row, col, moves)
        
        return moves

    """
    These helper functions contain the logic for calculating the valid moves
    of a piece from a given position on the board.
    """
    
    def pawnMoveLogic(self, row: int, col: int, moves: list):
        pass
    
    
    def rookMoveLogic(self, row: int, col: int, moves: list):
        pass    
    
    
    def knightMoveLogic(self, row: int, col: int, moves: list):
        pass
    
    
    def bishopMoveLogic(self, row: int, col: int, moves: list):
        pass
    
    
    def queenMoveLogic(self, row: int, col: int, moves: list):
        pass
    
    
    def kingMoveLogic(self, row: int, col: int, moves: list):
        pass
    
    
class Move():
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
        
        # store all the information about the move for comparisons
        self.moveID = self.movedPiece + str(self.startRow) + str(self.startCol) \
                      + str(self.destinationRow) + str(self.destinationCol) \
                      + self.capturedPiece
        
        print(self.moveID)
            
    def __eq__(self, other):
        """
        Overloading the "=" operator and defining what it means for 2 moves 
        to be the same so we can verify if a user's input is a legal move.
        """
        
        # make sure it only compares to other Move objects.
        if isinstance(other, Move):
            
            # compare the information
            return self.moveID == other.moveID
        
        return False
    
    
    
    
    
    
    
    
    