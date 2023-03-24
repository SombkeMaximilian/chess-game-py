# -*- coding: utf-8 -*-

class GameState():
    
    """
    This class stores all the information about the game state. Legal moves, 
    the board, a log of moves, whose turn it is, etc.
    """
    
    def __init__(self):
        
        self.board = Board()
        self.players = ["white", "black"]
        self.turnPlayer = "white"
        self.moveLog = []
        self.checkmate = False
        self.stalemate = False
        
        self.activePieces = {p : [] for p in self.players}
        self.capturedPieces = {p : [] for p in self.players}
        
        whiteRook1 = Rook(7, 0, "white")
        whiteRook2 = Rook(7, 7, "white")
        whiteKnight1 = Knight(7, 1, "white")
        whiteKnight2 = Knight(7, 6, "white")
        whiteBishop1 = Bishop(7, 5, "white")
        whiteBishop2 = Bishop(7, 2, "white")
        whiteQueen = Queen(7, 3, "white")
        whiteKing = King(7, 4, "white")
        whitePawn1 = Pawn(6, 0, "white")
        whitePawn2 = Pawn(6, 1, "white")
        whitePawn3 = Pawn(6, 2, "white")
        whitePawn4 = Pawn(6, 3, "white")
        whitePawn5 = Pawn(6, 4, "white")
        whitePawn6 = Pawn(6, 5, "white")
        whitePawn7 = Pawn(6, 6, "white")
        whitePawn8 = Pawn(6, 7, "white")
        
        self.activePieces["white"] = [
            whiteRook1, whiteRook2, whiteKnight1, whiteKnight2,
            whiteBishop1, whiteBishop2, whiteQueen, whiteKing,
            whitePawn1, whitePawn2, whitePawn3, whitePawn4,
            whitePawn5, whitePawn6, whitePawn7, whitePawn8           
            ]
        
        blackRook1 = Rook(0, 0, "black")
        blackRook2 = Rook(0, 7, "black")
        blackKnight1 = Knight(0, 1, "black")
        blackKnight2 = Knight(0, 6, "black")
        blackBishop1 = Bishop(0, 5, "black")
        blackBishop2 = Bishop(0, 2, "black")
        blackQueen = Queen(0, 3, "black")
        blackKing = King(0, 4, "black")
        blackPawn1 = Pawn(1, 0, "black")
        blackPawn2 = Pawn(1, 1, "black")
        blackPawn3 = Pawn(1, 2, "black")
        blackPawn4 = Pawn(1, 3, "black")
        blackPawn5 = Pawn(1, 4, "black")
        blackPawn6 = Pawn(1, 5, "black")
        blackPawn7 = Pawn(1, 6, "black")
        blackPawn8 = Pawn(1, 7, "black")
        
        self.activePieces["black"] = [
            blackRook1, blackRook2, blackKnight1, blackKnight2,
            blackBishop1, blackBishop2, blackQueen, blackKing,
            blackPawn1, blackPawn2, blackPawn3, blackPawn4,
            blackPawn5, blackPawn6, blackPawn7, blackPawn8
            ]
        
        self.board.addPieces(self.activePieces["white"] + self.activePieces["black"])
        self.kings = {"white": whiteKing, "black": blackKing}
        
    
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
        Generates all the moves the turn player can make while accounting
        for checks. Only handles moves of pieces other than The king. 
        Preventing moves from the king that put the king in check are 
        handled in the king class.
        """
        
        moves = []
        
        checks = self.getChecksAndSetPins()
        
        if self.kings[self.turnPlayer].inCheck == True:
            
            # 1 check still allows other pieces to make moves
            if len(checks) == 1:
            
                # generate all moves first
                moves = self.generateAllMoves()
                
                # non-king pieces can only move to these coordinates
                validSquares = []
                
                checkingPiece = checks[0][0]
                checkDirection = checks[0][1]
                
                # if a non-king piece moves, it must capture checking knight
                if checkingPiece.pieceType == "Knight":
            
                    validSquares = [(checkingPiece.row, checkingPiece.col)]
                    
                # pieces other than knights can be blocked or captured
                else:
                    
                    row = self.kings[self.turnPlayer].row
                    col = self.kings[self.turnPlayer].col
                    
                    # squares to block the check or capture attacking piece
                    while row != checkingPiece.row or col != checkingPiece.col:
                        
                        row += checkDirection[0]
                        col += checkDirection[1]
                        
                        validSquares.append((row, col))
                
                # remove all moves of other pieces that do not get the king out of check
                for i in range(len(moves) - 1, -1, -1):
                    
                    if moves[i].movedPiece.pieceType != "King":
                        
                        if not (moves[i].destinationRow, moves[i].destinationCol) in validSquares:
                            
                            moves.pop(i)
                
            # more than 1 check can only be dealt with by moving the king
            else:
                
                self.kings[self.turnPlayer].appendMoves(self.board, moves, self)

        # king is not in check, all moves are allowed
        else:
            
            moves = self.generateAllMoves()
        
        # if there are no legal moves for the turn player, the game ends
        if len(moves) == 0:
            
            if self.kings[self.turnPlayer].inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        
        else:
            
            self.checkmate = False
            self.stalemate = False
        
        return moves


    def generateAllMoves(self):
        
        """
        Generates all possible moves for the turn player.
        """
        
        moves = []
                
        for piece in self.activePieces[self.turnPlayer]:
            
            # calculating king moves requires the game state for checks
            if piece.pieceType != "King":
                piece.appendMoves(self.board, moves)
            else:
                piece.appendMoves(self.board, moves, self)
                
        return moves
    
    
    def getChecksAndSetPins(self, checksOnly = False):
        
        """
        Function that looks for any pins and checks of the turn player. First
        check in all linear directions away from the king to cover attack 
        directions of all normal pieces, then check separately for knights.
        Returns a list of tuples containing the checking piece as well as the
        direction it's checking the king from. Combining checks and pins into
        one function makes sense because it's necessary to verify whether an
        attacking piece gets blocked by another piece. Any allied blocking 
        piece is also pinned. Setting checksOnly to True is used for the king
        moves.
        """
        
        # all directions from which a Rook, Bishop or Queen could attack
        unitVectors = [(1, 0), (-1, 0), (0, 1), (0, -1),  
                       (1, 1), (-1, 1), (1, -1), (-1, -1)]
        
        
        # all relative coordinates from which a knight could attack
        knightCoordinates = [(2, 1), (-2, 1), (2, -1), (-2, -1), 
                             (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        checks = []
        
        # reset all pins
        if not checksOnly:
            for piece in self.activePieces[self.turnPlayer]:
                piece.resetPin()
        
        self.kings[self.turnPlayer].inCheck = False
        row = self.kings[self.turnPlayer].row
        col = self.kings[self.turnPlayer].col
        
        # check in all directions away from the king
        for u in unitVectors:
            
            possiblePin = None
            distanceFromKing = 1
            currRow = row + u[0]
            currCol = col + u[1]
            
            # keep going in that direction until the end of the board at most
            while 0 <= currRow <= 7 and 0 <= currCol <= 7:
                
                # check if there is an allied piece on that square
                if self.board.isAlly(currRow, currCol, self.turnPlayer):
                    
                    # no possible pin yet
                    if not possiblePin:
                        
                        # piece might be pinned
                        possiblePin = self.board[currRow, currCol]
                    
                    # 2 allied pieces, no pin or check in that direction
                    else:
                        
                        break
                
                # check if there is an enemy piece on that square
                elif self.board.isEnemy(currRow, currCol, self.turnPlayer):
                    
                    # check if it's a sliding piece that can attack in this 
                    # direction, negating the vector is not necessary (symmetry)
                    if u in self.board[currRow, currCol].unitVectors:
                        
                        # no allied piece is blocking the enemy sliding piece
                        if not possiblePin:
                            
                            checks.append((self.board[currRow, currCol], u))
                            break
                            
                        # allied piece is blocking the check, it is now pinned
                        else:
                            
                            if not checksOnly:
                                possiblePin.pinned = True
                                possiblePin.pinDirection = u
                            break
                    
                    # check if there is a king or pawn that can attack the turn
                    # player's king, negating the vector is necessary (pawns 
                    # move only in one direction)
                    elif (-u[0], -u[1]) in self.board[currRow, currCol].relativeCoordinates and \
                         distanceFromKing == 1:
                         
                        checks.append((self.board[currRow, currCol], u))
                        break
                    
                    # enemy pieces beyond the first in that direction are blocked
                    else:
                        break
                    
                distanceFromKing += 1
                currRow += u[0]
                currCol += u[1]
    
    
        # knights move in a special pattern, they also can't pin other pieces
        for k in knightCoordinates:
            
            currRow = row + k[0]
            currCol = col + k[1]
            
            # make sure it's a square on the board
            if 0 <= currRow <= 7 and 0 <= currCol <= 7:
                
                # check if it's an enemy piece
                if self.board.isEnemy(currRow, currCol, self.turnPlayer):    
                    
                    # check if it's a knight
                    if self.board[currRow, currCol].pieceType == "Knight":
                        
                        checks.append((self.board[currRow, currCol], k))
        
        if checks: 
            
            self.kings[self.turnPlayer].inCheck = True
        
        return checks
    
    
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
        
        """
        Adds a list of piece objects to the board, maybe useful for loading
        chess puzzles in the future.
        """
        
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
        
        """
        Check if the square at (row, col) is unoccupied.
        """
        
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
        Check if the square at (row, col) is occupied by an allied piece.
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
        if self.movedPiece != None:
            self.firstMove = not self.movedPiece.hasMoved
        
        # store all the information about the move for comparisons
        self.moveID = str(self.movedPiece) + str(self.startRow) + str(self.startCol) \
                      + str(self.destinationRow) + str(self.destinationCol) \
                      + str(self.capturedPiece)
    
        
    def __eq__(self, other):
        
        # make sure it only compares to other Move objects
        if isinstance(other, Move):
            
            # compare the information
            return self.moveID == other.moveID
        
        else:
            
            raise TypeError("Comparison between move and " + type(other) + " not supported.")

class Piece():
    
    def __init__(self, pieceType, row, col, player):
        
        self.pieceType = pieceType
        self.row = row
        self.col = col
        self.player = player
        self.hasMoved = False
        
        self.unitVectors = []
        self.relativeCoordinates = []
    
        self.pinned = False
        self.pinDirection = ()
    
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
        
    
    def slidingMoves(self, board, pattern):
        
        """
        Blueprint for calculating moves of Rooks, Bishops and Queens.
        """
        
        moves = []
        
        # check each direction
        for u in self.unitVectors:
            
            # pinned sliding pieces can only move along the line of the pin
            if self.pinned and self.pinDirection != u and self.pinDirection != (-u[0], -u[1]):
                continue
            
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
                    
                    # cannot jump over other pieces
                    break
                
                # neither empty nor an enemy piece, it's an allied piece
                else:
                    
                    # cannot jump over other pieces
                    break
                
                destRow += u[0]
                destCol += u[1]

        return moves
        
    
    def singleCoordinateMoves(self, board, relativeCoordinates):
        
        """
        Blueprint for calculating moves of Knights and Kings.
        """
        
        moves = []
        
        # pinned knight can never move, king cannot be pinned
        if self.pinned:
            return moves
        
        # check all relative coordinates
        for c in relativeCoordinates:
            
            # destination coordinates of the move
            destRow = self.row + c[0]
            destCol = self.col + c[1]
            
            # make sure the destination is a square on the board
            if 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check if that square doesn't contain an allied piece
                if not board.isAlly(destRow, destCol, self.player):
                    
                    # add moving to that square
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
        
        return moves
    
    
    def resetPin(self):
        
        self.pinned = False
        self.pinDirection = ()
    

class Pawn(Piece):
    
    def __init__(self, row, col, player):
        
        super().__init__("Pawn", row, col, player)
        
        # pawn move direction (white up, black down)
        if self.player == "white" : d = -1
        else :                      d = 1
        
        self.relativeCoordinates = [(d, 1), (d, -1)]  # capturing
        self.peaceful = (d, 0)                        # non-capturing
        
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the pawn can make from its current position on the
        board to the list moves.
        """
        
        u = self.peaceful[0]
        
        # pinned pawns can only move along the line of the pin
        if not self.pinned or self.pinDirection == self.peaceful or \
            self.pinDirection == (-self.peaceful[0], self.peaceful[1]):
            
            # check if the square in front is empty
            if board.isEmpty(self.row + u, self.col):
                
                # add moving 1 square forward as a legal move
                moves.append(Move((self.row, self.col), 
                                  (self.row+u, self.col), 
                                  board))
                
                # pawns can move 2 squares if they haven't moved yet
                if not self.hasMoved:
                       
                       # check if that square is empty
                       if board.isEmpty(self.row + 2 * u, self.col):
                           
                           # add moving 2 squares forward as a legal move
                           moves.append(Move((self.row, self.col), 
                                             (self.row+2*u, self.col), 
                                             board))
    
        
        # check the capture squares
        for c in self.relativeCoordinates:
            
            # pinned pawns can only capture the pinning piece
            if self.pinned and self.pinDirection != c:
                continue
            
            # destination coordinates of the move
            destRow = self.row + c[0]
            destCol = self.col + c[1]
            
            # make sure the destination is a square on the board
            if 0 <= destRow <= 7 and 0 <= destCol <= 7:
                
                # check if that square contains an enemy piece
                if board.isEnemy(destRow, destCol, self.player):
                    
                    # add moving to that square
                    moves.append(Move((self.row, self.col), (destRow, destCol), board))
        
        return
    
    
class Rook(Piece):
    
    def __init__(self, row, col, player):
        
        super().__init__("Rook", row, col, player)
        self.unitVectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def appendMoves(self, board, moves):
        
        """
        Appends all moves the rook can make from its current position on the
        board to the list moves.
        """

        moves += self.slidingMoves(board, self.unitVectors)

        return


class Bishop(Piece):

    def __init__(self, row, col, player):
        
        super().__init__("Bishop", row, col, player)
        self.unitVectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def appendMoves(self, board, moves):
        
        """
        Appends all moves the bishop can make from its current position on the
        board to the list moves.
        """

        moves += self.slidingMoves(board, self.unitVectors)

        return


class Queen(Piece):

    def __init__(self, row, col, player):
        
        super().__init__("Queen", row, col, player)
        self.unitVectors = [(1, 0), (-1, 0), (0, 1), (0, -1),
                            (1, 1), (-1, 1), (1, -1), (-1, -1)]
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the queen can make from its current position on the
        board to the list moves.
        """

        moves += self.slidingMoves(board, self.unitVectors)

        return


class Knight(Piece):

    def __init__(self, row, col, player):
        
        super().__init__("Knight", row, col, player)
        self.relativeCoordinates = [(2, 1), (-2, 1), (2, -1), (-2, -1), 
                                    (1, 2), (1, -2), (-1, 2), (-1, -2)]

    def __str__(self):
        
        return self.player[0] + "N"
    
    
    def appendMoves(self, board, moves):
        
        """
        Appends all moves the knight can make from its current position on the
        board to the list moves.
        """
    
        moves += self.singleCoordinateMoves(board, self.relativeCoordinates)
                    
        return


class King(Piece):
    
    def __init__(self, row, col, player):
        
        super().__init__("King", row, col, player)
        self.relativeCoordinates = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                                    (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.inCheck = False
                
    
    def appendMoves(self, board, moves, gamestate):
        
        """
        Appends all moves the knight can make from its current position on the
        board to the list moves.
        """
        
        kingMoves = self.singleCoordinateMoves(board, self.relativeCoordinates)
        
        for i in range(len(kingMoves) - 1, -1, -1):
            
            # move the king there and save the current inCheck value
            self.row = kingMoves[i].destinationRow
            self.col = kingMoves[i].destinationCol
            previousCheckState = self.inCheck
            
            # check if that move leaves the kind in check
            gamestate.getChecksAndSetPins(checksOnly = True)
            
            # revert back to original position
            self.row = kingMoves[i].startRow
            self.col = kingMoves[i].startCol
            
            # remove the move if the king is in check
            if self.inCheck:
                kingMoves.pop(i)
            
            # revert to previous inCheck value
            self.inCheck = previousCheckState
        
        moves += kingMoves
                    
        return