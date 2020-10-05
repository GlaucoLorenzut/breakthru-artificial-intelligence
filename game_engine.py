import textwrap
import game_ai

# logic of turn
G_1 = 0
G_2 = 1
S_1 = 2
S_2 = 3

class GameEngine():


    def __init__(self, ai_behaviour=None):
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sS", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "gS", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "gF", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sS", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sS", "sS", "sS", "sS", "sS", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "sS", "--", "--", "gS", "gS", "gS", "--", "--", "sS", "--"],
            ["--", "sS", "--", "gS", "--", "--", "--", "gS", "--", "sS", "--"],
            ["--", "sS", "--", "gS", "--", "gF", "--", "gS", "--", "sS", "--"],
            ["--", "sS", "--", "gS", "--", "--", "--", "gS", "--", "sS", "--"],
            ["--", "sS", "--", "--", "gS", "gS", "gS", "--", "--", "sS", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sS", "sS", "sS", "sS", "sS", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        #self.gold_turn = True
        #self.first_move = None

        self.turn = G_1
        self.game_log = []
        self.restore_log = []
        self.is_first_move = True
        self.valid_moves = self.get_all_possible_moves()
        self.ai = game_ai.AI(self.board, ai_behaviour)



    def is_valid_piece(self, r, c):
        if self.board[r][c] == "--":
            return False
        else:
            return True


    def is_gold_turn(self):
        return (self.turn==G_1 or self.turn==G_2)


    def is_piece_of_right_turn(self, r, c):
        piece_color = self.board[r][c][0]
        if (piece_color == 'g' and self.is_gold_turn()) or (piece_color == 's' and not self.is_gold_turn()):
            return True
        return False


    def update_turn(self, move):
        self.turn = (self.turn + move.cost) % 4
        self.is_first_move = False
        #print("( " + str(self.move_cost) + " + "+ str(move.cost) +" )")
        #print(self.turn)

        #print(str(self.turn) + "\n")
        #if self.move_cost + move.cost < 2:
        #    self.move_cost = self.move_cost + move.cost
        #    self.first_move = move
        #elif self.move_cost + move.cost == 2:
        #    self.gold_turn = not self.gold_turn
        #    self.move_cost = 0
        #    self.first_move = None
        #else:
        #    print("ERROR: too many moves ( " + str(self.move_cost) + " + "+ str(move.cost) +" )")


    def reset_turn(self, move):
        self.turn = (self.turn - move.cost) % 4
        #print("( " + str(self.move_cost) + " + "+ str(move.cost) +" )")
        #if self.move_cost - move.cost < 2:
        #    self.move_cost = self.move_cost + move.cost
        #    self.first_move = move
        #elif self.move_cost + move.cost == 2:
        #    self.gold_turn = not self.gold_turn
        #    self.move_cost = 0
        #    self.first_move = None
        #else:
        #    print("ERROR: too many moves ( " + str(self.move_cost) + " + "+ str(move.cost) +" )")


    def make_move(self, move):
        if move.ID != "skip":
            self.board[move.start_r][move.start_c] = "--"
            self.board[move.end_r][move.end_c] = move.piece_moved
        self.game_log.append(move)
        self.update_turn(move)
        self.restore_log = []

        self.update_all_possible_moves()
        return move.ID


    def skip_move(self):
        skip = Move((1,1),(1,1),self.board)
        skip.init_skip_move()
        self.game_log.append(skip)
        self.update_turn(skip)
        self.restore_log = []

        self.update_all_possible_moves()
        return skip.ID


    def undo_move(self):
        if len(self.game_log) > 0:
            last_move = self.game_log.pop()  # take and remove in one passage

            if last_move.ID != "skip":
                self.board[last_move.start_r][last_move.start_c] = last_move.piece_moved
                self.board[last_move.end_r][last_move.end_c] = last_move.piece_captured
            self.reset_turn(last_move)
            self.restore_log.append(last_move)

            self.update_all_possible_moves()

            if len(self.game_log) == 0:
                self.is_first_move = True

            return last_move.ID
        else:
            self.is_first_move = True
            return None


    def restore_move(self):
        if len(self.restore_log) > 0:
            restore_move = self.restore_log.pop()  # take and remove in one passage

            if restore_move.ID != "skip":
                self.board[restore_move.start_r][restore_move.start_c] = "--"
                self.board[restore_move.end_r][restore_move.end_c] = restore_move.piece_moved
            self.update_turn(restore_move)
            self.game_log.append(restore_move)

            self.update_all_possible_moves()
            return restore_move.ID


    def get_all_possible_moves(self): # not used anymore directly
        moves = []

        if self.is_first_move:
            skip = Move((1, 1), (1, 1), self.board)
            skip.init_skip_move()
            moves.append(skip)

        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):
                if self.is_piece_of_right_turn(r, c):
                    self.get_piece_moves(r, c, moves)
        return moves


    def update_all_possible_moves(self):
        self.valid_moves = self.get_all_possible_moves()


    def get_piece_moves(self, r, c, moves):
        if len(self.game_log)>0:
            fm_r, fm_c = self.game_log[-1].get_end_pos()
            if r == fm_r and c == fm_c:
                return

        # moves
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for d in directions:
            for i in range(1, len(self.board)+1):
                end_r = r + d[0] * i
                end_c = c + d[1] * i

                if 0 <= end_r < len(self.board) and 0 <= end_c < len(self.board):
                    endPiece = self.board[end_r][end_c]
                    if endPiece == '--':
                        move = Move((r, c), (end_r, end_c), self.board)
                        if self.has_feasible_cost(move):
                            moves.append(move)
                    else: # other piece
                        break
                else: # off board
                    break

        # captures
        if self.turn == G_2 or self.turn == S_2: #optimization
            return

        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        enemy_color = 's' if self.is_gold_turn() else 'g'
        for d in directions:
            end_r = r + d[0]
            end_c = c + d[1]
            if 0 <= end_r < len(self.board) and 0 <= end_c < len(self.board):
                endPiece = self.board[end_r][end_c][0]
                if endPiece == enemy_color:
                    move = Move((r, c), (end_r, end_c), self.board)
                    moves.append(move)


    def has_feasible_cost(self,move):
        return (move.cost == 1 or self.turn == G_1 or self.turn == S_1)


    def check_single_piece_moves(self, r, c): #subset of self.valid_moves
        move_list, capture_list = [], []
        for move in self.valid_moves:
            if move.start_r == r and move.start_c == c:
                if move.piece_captured != "--":
                    capture_list.append(move)
                else:
                    move_list.append(move)
        return move_list, capture_list


    def check_victory(self):
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
        return "GAME"


    def print_board(self):
        string = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                string += self.board[i][j] + "  "
            print(string + "\n")
            string = ""



class Move():
    ranks_to_rows = {
        "1": 10, "2": 9,
        "3": 8, "4": 7,
        "5": 6, "6": 5,
        "7": 4, "8": 3,
        "9": 2, "10": 1,
        "11": 0
    }

    rows_to_ranks = {
        v : k for k, v in ranks_to_rows.items()
    }

    files_to_cols = {
        "a": 0, "b": 1,
        "c": 2, "d": 3,
        "e": 4, "f": 5,
        "g": 6, "h": 7,
        "i": 8, "j": 9,
        "k": 10
    }

    cols_to_files = {
        v : k for k, v in files_to_cols.items()
    }

    def __init__(self, start_sq, end_sq, board):
        self.start_r = start_sq[0]
        self.start_c = start_sq[1]
        self.end_r = end_sq[0]
        self.end_c = end_sq[1]
        self.piece_moved = board[self.start_r][self.start_c]
        self.piece_captured = board[self.end_r][self.end_c]
        self.cost = 2 if (self.piece_captured != "--" or self.piece_moved == "gF") else 1
        self.ID = self.get_chess_notation()

    def init_skip_move(self): #SKIP MOVE
        self.start_r        = None
        self.start_c        = None
        self.end_r          = None
        self.end_c          = None
        self.piece_moved    = "--"
        self.piece_captured = "--"
        self.cost = 2
        self.ID = "skip"


    def __eq__(self, other): # overriding ==
        if isinstance(other, Move):
            return self.ID == other.ID
        return False


    def get_start_pos(self):
        return (self.start_r, self.start_c)


    def get_end_pos(self):
        return (self.end_r, self.end_c)


    def get_chess_notation(self):
        return self.get_rank_file(self.start_r, self.start_c) + "-" +  self.get_rank_file(self.end_r, self.end_c)


    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def is_capture_move(self):
        return True if self.piece_captured != "--" else False

    def is_capture_flag(self):
        return True if self.piece_captured == "gF" else False



if __name__ == "__main__":
    number = 9
    board_A = "{:064b}".format(number)
    board_B = "{:064b}".format(0)
    board = (board_A, board_B)


    def print_board(board):
        print('\n'.join([' '.join(textwrap.wrap(line, 1)) for line in textwrap.wrap(board[0], 11)]))

    print_board(board)
