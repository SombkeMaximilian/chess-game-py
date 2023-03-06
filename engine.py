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
        
        # keeps track of which rooks can still be used for castling
        self.whiteCastling = [True, True]
        self.blackCastling = [True, True]
        
        self.players = ["w", "b"]
        self.turnPlayer = "w"
        self.moveLog = []
        
    
    def switchTurn(self):
        """
        Changes the turn player.
        """
        
        self.turnPlayer = [player for player in self.players 
                           if player != self.turnPlayer][0]
        
    
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
        self.switchTurn()
        
    
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
            self.switchTurn()
    
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
        moves = []
        
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
        """
        Calculates all moves a pawn on a given row and column can make.
        """
        
        # white pawns move up, black pawns move down
        if self.turnPlayer == "w":
            u = -1
        elif self.turnPlayer == "b":
            u = 1    
        
        # check if square in front of the pawn is empty
        if self.board[row+u][col] == "em":
            
            # add moving 1 square forward as a legal move
            moves.append(Move((row, col), (row+u, col), self.board))
            
            # pawns can move 2 squares if they haven't moved yet
            if (row == 6 and self.turnPlayer == "w") or \
               (row == 1 and self.turnPlayer == "b"):
                
                # check if that square is empty
                if self.board[row+2*u][col] == "em":
                    
                    # add moving 2 squares forward as a legal move
                    moves.append(Move((row, col), (row+2*u, col), self.board))
            
        # make sure the pawn isn't in the far left column to avoid errors
        if col - 1 >= 0:
       
                # check if the forward diagonally to the left square contains an enemy piece
                if self.board[row+u][col-1][0] != self.turnPlayer:
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((row, col), (row+u, col-1), self.board))
                    
        # make sure the pawn isn't in the far right column to avoid errors
        if col + 1 <= 7:
            
                # check if the forward diagonally to the right square contains an enemy piece
                if self.board[row+u][col+1][0] != self.turnPlayer:
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((row, col), (row+u, col+1), self.board))
                    
    
    def rookMoveLogic(self, row: int, col: int, moves: list):
        """
        Calculates all moves a rook on a given row and column can make.
        """
        
        unitVectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        # check each direction
        for u in unitVectors:
            
            destRow = row + u[0]
            destCol = col + u[1]
            
            # keep going in that direction until the end of the board at most
            while 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check for empty squares along the way
                if self.board[destRow][destCol] == "em":
                    
                    # add all of those as legal moves
                    moves.append(Move((row, col), (destRow, destCol), self.board))
                
                # check for enemy pieces along the way
                elif self.board[destRow][destCol][0] != self.turnPlayer:
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((row, col), (destRow, destCol), self.board))
                    
                    # rooks cannot jump over other pieces
                    break
                
                # neither empty nor an enemy piece, it's an allied piece
                else:
                    
                    # rooks cannot jump over other pieces
                    break
                
                destRow += u[0]
                destCol += u[1]
                
    
    def knightMoveLogic(self, row: int, col: int, moves: list):
        """
        Calculates all moves a knight on a given row and column can make.
        """
        
        coordinateChange = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        # check all knight moves
        for c in coordinateChange:
            
            # destination coordinates of the move
            destRow = row + c[0]
            destCol = col + c[1]
            
            # make sure the destination is a square on the board
            if 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check if that square contains an allied piece
                if self.board[destRow][destCol][0] != self.turnPlayer:
                    
                    # add moving to that square (empty or contains enemy piece)
                    moves.append(Move((row, col), (destRow, destCol), self.board))
        
    
    def bishopMoveLogic(self, row: int, col: int, moves: list):
        """
        Calculates all moves a bishop on a given row and column can make.
        """        
        
        unitVectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        
        # check each direction
        for u in unitVectors:
            
            destRow = row + u[0]
            destCol = col + u[1]
            
            # keep going in that direction until the end of the board at most
            while 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check for empty squares along the way
                if self.board[destRow][destCol] == "em":
                    
                    # add all of those as legal moves
                    moves.append(Move((row, col), (destRow, destCol), self.board))
                
                # check for enemy pieces along the way
                elif self.board[destRow][destCol][0] != self.turnPlayer:
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((row, col), (destRow, destCol), self.board))
                    
                    # rooks cannot jump over other pieces
                    break
                
                # neither empty nor an enemy piece, it's an allied piece
                else:
                    
                    # rooks cannot jump over other pieces
                    break
                
                destRow += u[0]
                destCol += u[1]
    
    
    def queenMoveLogic(self, row: int, col: int, moves: list):
        """
        Calculates all moves a queen on a given row and column can make.
        """        
        
        # a queen can make exactly the moves both a rook and bishop can make
        self.rookMoveLogic(row, col, moves)
        self.bishopMoveLogic(row, col, moves)
    
    
    def kingMoveLogic(self, row: int, col: int, moves: list):
        """
        Calculates all moves a king on a given row and column can make.
        """        
        
        coordinateChange = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        # check all king moves
        for c in coordinateChange:
            
            # destination coordinates of the move
            destRow = row + c[0]
            destCol = col + c[1]
            
            # make sure the destination is a square on the board
            if 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check if that square contains an allied piece
                if self.board[destRow][destCol][0] != self.turnPlayer:
                    
                    # add moving to that square (empty or contains enemy piece)
                    moves.append(Move((row, col), (destRow, destCol), self.board))
    
    
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
    
    
    
    
    
    
    
    
    