# -*- coding: utf-8 -*-

class GameState():
    
    """
    This class stores all the information about the game state. Legal moves, the board, a log of 
    moves, whose turn it is, etc.
    """
    
    def __init__(self):
        
        self.board = Board()
        self.players = ["white", "black"]
        self.turnPlayer = "white"
        self.moveLog = []
        
        self.activePieces = {p : [] for p in self.players}
        self.capturedPieces = {p : [] for p in self.players}
        
        whiteRook1 = Rook("Rook", 7, 0, "white")
        whiteRook2 = Rook("Rook", 7, 7, "white")
        whiteKnight1 = Knight("Knight", 7, 1, "white")
        whiteKnight2 = Knight("Knight", 7, 6, "white")
        whiteBishop1 = Bishop("Bishop", 7, 5, "white")
        whiteBishop2 = Bishop("Bishop", 7, 2, "white")
        whiteQueen = Queen("Queen", 7, 3, "white")
        whiteKing = King("King", 7, 4, "white")
        whitePawn1 = Pawn("Pawn", 6, 0, "white")
        whitePawn2 = Pawn("Pawn", 6, 1, "white")
        whitePawn3 = Pawn("Pawn", 6, 2, "white")
        whitePawn4 = Pawn("Pawn", 6, 3, "white")
        whitePawn5 = Pawn("Pawn", 6, 4, "white")
        whitePawn6 = Pawn("Pawn", 6, 5, "white")
        whitePawn7 = Pawn("Pawn", 6, 6, "white")
        whitePawn8 = Pawn("Pawn", 6, 7, "white")
        
        self.activePieces["white"] = [
            whiteRook1, whiteRook2, whiteKnight1, whiteKnight2,
            whiteBishop1, whiteBishop2, whiteQueen, whiteKing,
            whitePawn1, whitePawn2, whitePawn3, whitePawn4,
            whitePawn5, whitePawn6, whitePawn7, whitePawn8           
            ]
        
        blackRook1 = Rook("Rook", 0, 0, "black")
        blackRook2 = Rook("Rook", 0, 7, "black")
        blackKnight1 = Knight("Knight", 0, 1, "black")
        blackKnight2 = Knight("Knight", 0, 6, "black")
        blackBishop1 = Bishop("Bishop", 0, 5, "black")
        blackBishop2 = Bishop("Bishop", 0, 2, "black")
        blackQueen = Queen("Queen", 0, 3, "black")
        blackKing = King("King", 0, 4, "black")
        blackPawn1 = Pawn("Pawn", 1, 0, "black")
        blackPawn2 = Pawn("Pawn", 1, 1, "black")
        blackPawn3 = Pawn("Pawn", 1, 2, "black")
        blackPawn4 = Pawn("Pawn", 1, 3, "black")
        blackPawn5 = Pawn("Pawn", 1, 4, "black")
        blackPawn6 = Pawn("Pawn", 1, 5, "black")
        blackPawn7 = Pawn("Pawn", 1, 6, "black")
        blackPawn8 = Pawn("Pawn", 1, 7, "black")
        
        self.activePieces["black"] = [
            blackRook1, blackRook2,
            blackKnight1, blackKnight2,
            blackBishop1, blackBishop2,
            blackQueen, blackKing,
            blackPawn1, blackPawn2, blackPawn3, blackPawn4,
            blackPawn5, blackPawn6, blackPawn7, blackPawn8
            ]
        
        self.board.addPieces(self.activePieces["white"] + self.activePieces["black"])
    
    def switchTurn(self):
        
        """
        Changes the turn player.
        """
        
        self.turnPlayer = [player for player in self.players 
                           if player != self.turnPlayer][0]
    
    
    def performMove(self, move):
        
        """
        Updates information of pieces and board to reflect that a move was
        performed.
        """
        
        # update information of the piece
        move.movedPiece.movePiece(move)
        
        # update board
        self.board.updateMove(move)
                
        # if a piece was captured, remove it from the list of active pieces
        if move.capturedPiece != None:
            
            self.activePieces[move.capturedPiece.player].remove(move.capturedPiece)
            self.capturedPieces[move.capturedPiece.player].append(move.capturedPiece)
        
        # add the move to the log
        self.moveLog.append(move)
        
        # change the turn player
        self.switchTurn()
        
    
    def undoMove(self):
        
        """
        Undo the last move.
        """
        
        # check if there is a move to undo (log is not empty)
        if self.moveLog:
            
            # grab the last move and remove it from the log
            lastMove = self.moveLog.pop(-1)
            
            # update information of the moved piece
            lastMove.movedPiece.undoMovePiece(lastMove)
            
            # update board
            self.board.updateUndo(lastMove)
            
            # if a piece was captured, add it back to the active pieces
            if lastMove.capturedPiece != None:
                
                self.activePieces[lastMove.capturedPiece.player].append(lastMove.capturedPiece)
                self.capturedPieces[lastMove.capturedPiece.player].remove(lastMove.capturedPiece)            

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
                
        # iterate over all squares on the board
        for piece in self.activePieces[self.turnPlayer]:
            
            piece.appendMoves(self.board, moves)
                
        return moves
    
    
class Board():
    
    def __init__(self):
        
        self.matrix = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
            ]
        
    
    def __setitem__(self, index, value):
        
        self.matrix[index[0]][index[1]] = value
    
    
    def __getitem__(self, index):
        
        return self.matrix[index[0]][index[1]]
    
    
    def __str__(self):
        
        outputString = ""
        
        for row in self.matrix:
            
            for element in row:
                
                if element != None:    
                
                    outputString += f"{str(element):4} "
            
                else:
                    
                    outputString += f"{'em':4} "
            
            outputString += "\n"
        
        return outputString
    
    
    def addPieces(self, pieces):
        
        for piece in pieces:
            
            self.matrix[piece.row][piece.col] = piece
    
        return
    
    
    def updateMove(self, move):
        
        """
        Updates board with a move.
        """
        
        self.matrix[move.startRow][move.startCol] = None
        self.matrix[move.destinationRow][move.destinationCol] = move.movedPiece
        
        return
    
    
    def updateUndo(self, move):
        
        """
        Reverts board back to before a move was performed.
        """
        
        self.matrix[move.startRow][move.startCol] = move.movedPiece
        self.matrix[move.destinationRow][move.destinationCol] = move.capturedPiece
    
        return
    
    
    def isEmpty(self, row, col):
        
        return self.matrix[row][col] == None
    
    
    def isEnemy(self, row, col, player):
        
        """
        Check if the square at (row, col) is occupied by an enemy piece.
        """
        
        if self.isEmpty(row, col):
            
            return False
        
        else:
            
            return self.matrix[row][col].player != player

    
    def isAlly(self, row, col, player):
        
        """
        Check if the square at (row, col) is occupied by an allied piece
        """
        
        if self.isEmpty(row, col):
            
            return False
        
        else:
            
            return self.matrix[row][col].player == player

class Move():
    
    """
    This class is responsible for calculating moves of pieces, it also stores
    the information about which piece was moved and which piece was captured,
    if any.
    """
    
    def __init__(self, start, destination, board):
        
        # store start position and destination
        self.startRow, self.startCol = start
        self.destinationRow, self.destinationCol = destination
        
        # store moved and captured pieces
        self.movedPiece = board[self.startRow, self.startCol]
        self.capturedPiece = board[self.destinationRow, self.destinationCol]
        
        # is this the piece's first move (important for pawns, castling, ..)
        if self.movedPiece.hasMoved == False:
            self.firstMove = True
        else:
            self.firstMove = False
        
        # store all the information about the move for comparisons
        self.moveID = str(self.movedPiece) + str(self.startRow) + str(self.startCol) \
                      + str(self.destinationRow) + str(self.destinationCol) \
                      + str(self.capturedPiece)
    
        
    def __eq__(self, other):
        
        # make sure it only compares to other Move objects.
        if isinstance(other, Move):
            
            # compare the information
            return self.moveID == other.moveID
        
        return False


class Piece():
    
    def __init__(self, pieceType, row, col, player):
        
        self.pieceType = pieceType
        self.row = row
        self.col = col
        self.player = player
        self.hasMoved = False
    
    
    def __str__(self):
        
        return self.player[0] + self.pieceType[0]
    
    
    def movePiece(self, move):
        
        """
        Update position to perform the move.
        """
        
        self.row = move.destinationRow
        self.col = move.destinationCol
        self.hasMoved = True
        
    
    def undoMovePiece(self, move):
        
        """
        Update position to undo the move.
        """
        
        self.row = move.startRow
        self.col = move.startCol
        self.hasMoved = not move.firstMove
        

class Pawn(Piece):
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the pawn can make from its current position on the
        board to the list moves.
        """

        # white pawns move up, black pawns move down
        if self.player == "white":
            u = -1
        elif self.player == "black":
            u = 1
        
        # check if the square in front is empty
        if board.isEmpty(self.row + u, self.col):
            
            # add moving 1 square forward as a legal move
            moves.append(Move((self.row, self.col), (self.row+u, self.col), board))
            
            # pawns can move 2 squares if they haven't moved yet
            if not self.hasMoved:
                   
                   # check if that square is empty
                   if board.isEmpty(self.row + 2 * u, self.col):
                       
                       # add moving 2 squares forward as a legal move
                       moves.append(Move((self.row, self.col), (self.row+2*u, self.col), board))
    
        # make sure the pawn isn't in the far left column to avoid errors
        if self.col - 1 >= 0:
       
                # check if the forward diagonally to the left square contains an enemy piece
                if board.isEnemy(self.row+u, self.col-1, self.player):
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((self.row, self.col), (self.row+u, self.col-1), board))
                    
        # make sure the pawn isn't in the far right column to avoid errors
        if self.col + 1 <= 7:
            
                # check if the forward diagonally to the right square contains an enemy piece
                if board.isEnemy(self.row+u, self.col+1, self.player):
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((self.row, self.col), (self.row+u, self.col+1), board))
        
        return
    
class Rook(Piece):
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the rook can make from its current position on the
        board to the list moves.
        """
        
        unitVectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        # check each direction
        for u in unitVectors:
            
            destRow = self.row + u[0]
            destCol = self.col + u[1]
            
            # keep going in that direction until the end of the board at most
            while 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check for empty squares along the way
                if board.isEmpty(destRow, destCol):
                    
                    # add all of those as legal moves
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                
                # check for enemy pieces along the way
                elif board.isEnemy(destRow, destCol, self.player):
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                    
                    # rooks cannot jump over other pieces
                    break
                
                # neither empty nor an enemy piece, it's an allied piece
                else:
                    
                    # rooks cannot jump over other pieces
                    break
                
                destRow += u[0]
                destCol += u[1]  

        return


class Bishop(Piece):
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the bishop can make from its current position on the
        board to the list moves.
        """
        
        unitVectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        
        # check each direction
        for u in unitVectors:
            
            destRow = self.row + u[0]
            destCol = self.col + u[1]
            
            # keep going in that direction until the end of the board at most
            while 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check for empty squares along the way
                if board.isEmpty(destRow, destCol):
                    
                    # add all of those as legal moves
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                
                # check for enemy pieces along the way
                elif board.isEnemy(destRow, destCol, self.player):
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                    
                    # bishops cannot jump over other pieces
                    break
                
                # neither empty nor an enemy piece, it's an allied piece
                else:
                    
                    # bishops cannot jump over other pieces
                    break
                
                destRow += u[0]
                destCol += u[1]  

        return


class Queen(Piece):
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the queen can make from its current position on the
        board to the list moves. A queen can make all moves that a rook or a
        bishop can make.
        """
        
        unitVectors = [(1, 0), (-1, 0), (0, 1), (0, -1),   # rook part
                       (1, 1), (-1, 1), (1, -1), (-1, -1)] # bishop part
        
        # check each direction
        for u in unitVectors:
            
            destRow = self.row + u[0]
            destCol = self.col + u[1]
            
            # keep going in that direction until the end of the board at most
            while 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check for empty squares along the way
                if board.isEmpty(destRow, destCol):
                    
                    # add all of those as legal moves
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                
                # check for enemy pieces along the way
                elif board.isEnemy(destRow, destCol, self.player):
                    
                    # add capturing that piece as a legal move
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                    
                    # queens cannot jump over other pieces
                    break
                
                # neither empty nor an enemy piece, it's an allied piece
                else:
                    
                    # queens cannot jump over other pieces
                    break
                
                destRow += u[0]
                destCol += u[1]  

        return


class Knight(Piece):
    
    def __str__(self):
        
        return self.player[0] + "N"
    
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the knight can make from its current position on the
        board to the list moves.
        """
        
        coordinateChange = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        # check all knight moves
        for c in coordinateChange:
            
            # destination coordinates of the move
            destRow = self.row + c[0]
            destCol = self.col + c[1]
            
            # make sure the destination is a square on the board
            if 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check if that square doesn't contain an allied piece
                if not board.isAlly(destRow, destCol, self.player):
                    
                    # add moving to that square
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                    
        return


class King(Piece):
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the knight can make from its current position on the
        board to the list moves.
        """
        
        coordinateChange = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        # check all knight moves
        for c in coordinateChange:
            
            # destination coordinates of the move
            destRow = self.row + c[0]
            destCol = self.col + c[1]
            
            # make sure the destination is a square on the board
            if 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check if that square doesn't contain an allied piece
                if not board.isAlly(destRow, destCol, self.player):
                    
                    # add moving to that square
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
                    
        return
        