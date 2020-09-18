import textwrap

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.gameLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.gameLog.append(move)
        self.whiteToMove = not self.whiteToMove
        print("move: " + move.getChessNotation())


    def undoMove(self):
        if len(self.gameLog) > 0:
            last_move = self.gameLog.pop()  # take and remove in one passage
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            print("undo: " + last_move.getChessNotation())

    def restoreMove(self):
        #TODO
        pass














class Move():
    ranksToRows = {
        "1": 7, "2": 6,
        "3": 5, "4": 4,
        "5": 3, "6": 2,
        "7": 1, "8": 0
    }
    rowsToRanks = {
        v : k for k, v in ranksToRows.items()
    }
    filesToCols = {
        "a": 0, "b": 1,
        "c": 2, "d": 3,
        "e": 4, "f": 5,
        "g": 6, "h": 7
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

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + "-" +  self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]



board = "{:064b}".format(2 | 1)

def print_board(board):
    print('\n'.join([' '.join(textwrap.wrap(line,1)) for line in textwrap.wrap(board, 8)]))

if __name__ == "__main__":
    print_board(board)