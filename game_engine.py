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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.gameLog.append(move)
        self.whiteToMove = not self.whiteToMove

        self.restoreLog = []
        print("move: " + move.getChessNotation())


    def undoMove(self):
        if len(self.gameLog) > 0:
            last_move = self.gameLog.pop()  # take and remove in one passage
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            self.restoreLog.append(last_move)
            print("undo: " + last_move.getChessNotation())

    def restoreMove(self):
        if len(self.restoreLog) > 0:
            restore_move = self.restoreLog.pop()  # take and remove in one passage

            self.board[restore_move.startRow][restore_move.startCol] = "--"
            self.board[restore_move.endRow][restore_move.endCol] = restore_move.pieceMoved
            self.whiteToMove = not self.whiteToMove
            self.gameLog.append(restore_move)
            print("restore: " + restore_move.getChessNotation())














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

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + "-" +  self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]



board = "{:064b}".format(2 | 1)

def print_board(board):
    print('\n'.join([' '.join(textwrap.wrap(line,1)) for line in textwrap.wrap(board, 8)]))

if __name__ == "__main__":
    print_board(board)