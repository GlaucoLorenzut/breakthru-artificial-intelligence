import textwrap


class GameState():


    def __init__(self):
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sS", "sS", "sS", "sS", "sS", "--", "--", "--"],
            ["--", "--", "gF", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "sS", "--", "--", "gS", "gS", "gS", "--", "--", "sS", "--"],
            ["--", "sS", "--", "gS", "--", "--", "--", "gS", "--", "sS", "--"],
            ["--", "sS", "--", "gS", "--", "--", "--", "gS", "--", "sS", "--"],
            ["--", "sS", "--", "gS", "--", "--", "--", "gS", "--", "sS", "--"],
            ["--", "sS", "--", "--", "gS", "gS", "gS", "--", "--", "sS", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sS", "sS", "sS", "sS", "sS", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.gold_turn = True
        self.gameLog = []
        self.restoreLog = []


    def isValidPiece(self, r, c):
        if self.board[r][c] == "--":
            return False
        else:
            return True

    def is_correct_turn(self, r, c):
        turn = self.board[r][c][0]
        if (turn == 'g' and self.gold_turn) or (turn == 's' and not self.gold_turn):
            return True
        return False


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.gameLog.append(move)
        self.gold_turn = not self.gold_turn #TODO

        self.restoreLog = []
        print("move: " + move.ID)
        #self.printBoard()


    def undoMove(self):
        if len(self.gameLog) > 0:
            last_move = self.gameLog.pop()  # take and remove in one passage
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.gold_turn = not self.gold_turn

            self.restoreLog.append(last_move)
            print("undo: " + last_move.ID)


    def restoreMove(self):
        if len(self.restoreLog) > 0:
            restore_move = self.restoreLog.pop()  # take and remove in one passage

            self.board[restore_move.startRow][restore_move.startCol] = "--"
            self.board[restore_move.endRow][restore_move.endCol] = restore_move.pieceMoved
            self.gold_turn = not self.gold_turn
            self.gameLog.append(restore_move)
            print("restore: " + restore_move.ID)


    def getAllPossibleMoves(self):
        #print("start")
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'g' and self.gold_turn) or (turn == 's' and not self.gold_turn): #TODO chec
                    self.getPieceMoves(r, c, moves)
        #print("end\n")
        return moves


    def getPieceMoves(self, r, c, moves):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        enemyColor = 's'if self.gold_turn else 'g'
        for d in directions:
            for i in range(1, len(self.board)+1):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else: # other piece
                        break
                else: # off board
                    break
        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                endPiece = self.board[endRow][endCol][0]
                if endPiece == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def check_single_piece_moves(self, r, c, all_valid_moves):
        move_list, capture_list = [], []
        for move in all_valid_moves:
            if move.startRow == r and move.startCol == c:
                if move.pieceCaptured != "--":
                    capture_list.append(move)
                else:
                    move_list.append(move)
        return move_list, capture_list


    def checkVictory(self):
        flagship_escaped = False
        flagship_killed = True

        # vertical check
        for i in range(len(self.board)):
            if self.board[i][0] == "gF" or self.board[i][len(self.board)-1] == "gF":
                flagship_escaped = True

        # horizontal check
        for j in range(len(self.board[0])):
            if self.board[0][j] == "gF" or self.board[len(self.board[0])-1][j] == "gF":
                flagship_escaped = True

        # kill check
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == "gF":
                    flagship_killed = False

        if flagship_escaped:
            return "GOLD_WIN"
        if flagship_killed:
            return "SILVER_WIN"
        return ""

    def printBoard(self):
        string = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                string += self.board[i][j] + "  "
            print(string + "\n")
            string = ""


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
        self.cost = 2 if (self.pieceCaptured != "--" or self.pieceMoved == "wK") else 1
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
