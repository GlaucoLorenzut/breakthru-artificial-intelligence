import textwrap

class GameState():
    def __init__(self):
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bR", "bR", "bR", "bR", "bR", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "bR", "--", "--", "wR", "wR", "wR", "--", "--", "bR", "--"],
            ["--", "bR", "--", "wR", "--", "--", "--", "wR", "--", "bR", "--"],
            ["--", "bR", "--", "wR", "--", "wK", "--", "wR", "--", "bR", "--"],
            ["--", "bR", "--", "wR", "--", "--", "--", "wR", "--", "bR", "--"],
            ["--", "bR", "--", "--", "wR", "wR", "wR", "--", "--", "bR", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bR", "bR", "bR", "bR", "bR", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.whiteToMove = True
        self.gameLog = []
        self.restoreLog = []

    def isValidPiece(self, row, col):
        if self.board[row][col] == "--":
            return False
        else:
            return True



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.gameLog.append(move)
        self.whiteToMove = not self.whiteToMove

        self.restoreLog = []
        print("move: " + move.ID)


    def undoMove(self):
        if len(self.gameLog) > 0:
            last_move = self.gameLog.pop()  # take and remove in one passage
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            self.restoreLog.append(last_move)
            print("undo: " + last_move.ID)

    def restoreMove(self):
        if len(self.restoreLog) > 0:
            restore_move = self.restoreLog.pop()  # take and remove in one passage

            self.board[restore_move.startRow][restore_move.startCol] = "--"
            self.board[restore_move.endRow][restore_move.endCol] = restore_move.pieceMoved
            self.whiteToMove = not self.whiteToMove
            self.gameLog.append(restore_move)
            print("restore: " + restore_move.ID)

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): #TODO chec
                    piece = self.board[r][c][1]
                    if piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)

        return moves



    def getRookMoves(self, row, col, moves):
        pass

    def getKingMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)










class Move():
    ranksToRows = {
        "1": 10, "2": 9,
        "3": 8, "4": 7,
        "5": 6, "6": 5,
        "7": 4, "8": 3,
        "9": 2, "10": 1,
        "11": 0
    }

    rowsToRanks = {
        v : k for k, v in ranksToRows.items()
    }

    filesToCols = {
        "a": 0, "b": 1,
        "c": 2, "d": 3,
        "e": 4, "f": 5,
        "g": 6, "h": 7,
        "i": 8, "j": 9,
        "k": 10
    }

    colsToFiles = {
        v : k for k, v in filesToCols.items()
    }

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.ID = self.getChessNotation()

    def __eq__(self, other): # overriding ==
        if isinstance(other, Move):
            return self.ID == other.ID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + "-" +  self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]


number = 9
board_A = "{:064b}".format(number)
board_B = "{:064b}".format(0)
board=(board_A, board_B)
def print_board(board):
    print('\n'.join([' '.join(textwrap.wrap(line, 1)) for line in textwrap.wrap(board[0], 11)]))

if __name__ == "__main__":
    print_board(board)