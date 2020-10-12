import textwrap
from random import seed
from random import randint
from datetime import datetime
import copy
import pygame

# logic of turn
G_1 = 0
G_2 = 1
S_1 = 2
S_2 = 3

# logic of pieces

F = 3  # FLAG
V = 0  # VOID
G = 1  # GOLD ship
S = 2  # SILVER ship

INFINITE = 1000000

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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, S, S, S, S, S, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, S, 0, 0, G, G, G, 0, 0, S, 0],
            [0, S, 0, G, 0, 0, 0, G, 0, S, 0],
            [0, S, 0, G, 0, F, 0, G, 0, S, 0],
            [0, S, 0, G, 0, 0, 0, G, 0, S, 0],
            [0, S, 0, 0, G, G, G, 0, 0, S, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, S, S, S, S, S, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.turn = G_1
        self.game_log = []
        self.restore_log = []
        self.is_first_move = True
        self.valid_moves = self.get_all_possible_moves()
        self.ai_behaviour = ai_behaviour
        self.ai_timer = 0


    # logic functions

    def is_valid_piece(self, r, c):
        return bool(self.board[r][c])


    def is_gold_turn(self):
        return (self.turn==G_1 or self.turn==G_2)


    def is_piece_of_right_turn(self, r, c):
        if not self.is_valid_piece(r, c):
            return False
        is_gold_turn = self.is_gold_turn()
        piece_color = self.board[r][c]%2 # pair are silver pieces
        if (piece_color == 1 and is_gold_turn) or (piece_color == 0 and not is_gold_turn):
            return True
        return False


    def has_feasible_cost(self,move):
        return (move.cost == 1 or self.turn == G_1 or self.turn == S_1)


    def is_flag_escaped(self):
        flagship_escaped = False

        # vertical check
        for i in range(len(self.board)):
            if self.board[i][0] == F or self.board[i][len(self.board)-1] == F:
                flagship_escaped = True

        # horizontal check
        for j in range(len(self.board[0])):
            if self.board[0][j] == F or self.board[len(self.board[0])-1][j] == F:
                flagship_escaped = True

        return flagship_escaped


    def get_number_of_ships(self):
        n_gold_flag, n_gold_ship, n_silver_ship = 0, 0, 0

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == G:
                    n_gold_ship += 1
                elif self.board[i][j] == S:
                    n_silver_ship += 1
                elif self.board[i][j] == F:
                    n_gold_flag = 1

        return (n_gold_flag, n_gold_ship, n_silver_ship)


    def distance_flag_from_edges(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == F:
                    y = min(i, len(self.board)-i-1)
                    x = min(j, len(self.board[0]) - j - 1)

        return (x, y)


    #active functions

    def update_turn(self, move):
        self.turn = (self.turn + move.cost) % 4
        self.is_first_move = False


    def reset_turn(self, move):
        self.turn = (self.turn - move.cost) % 4


    def make_move(self, move):
        if move.ID != "skip":
            self.board[move.start_r][move.start_c] = V
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
                self.board[restore_move.start_r][restore_move.start_c] = V
                self.board[restore_move.end_r][restore_move.end_c] = restore_move.piece_moved
            self.update_turn(restore_move)
            self.game_log.append(restore_move)

            self.update_all_possible_moves()
            return restore_move.ID


    def get_all_possible_moves(self):
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


    def get_all_possible_moves_AI(self): # return a dict of all possible moves in one turn
        move_list = []

        if self.is_first_move: # first in the whole game
            skip = Move((1, 1), (1, 1), self.board)
            skip.init_skip_move()
            move_list.append([skip])

        first_move_list = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):
                if self.is_piece_of_right_turn(r, c):
                    self.get_piece_moves(r, c, first_move_list)

        for first_move in first_move_list:
            if first_move.cost == 2:
                move_list.append([first_move])
            else:
                self.simulate_make_move(first_move)
                #self.turn += 1

                second_move_list = []
                for r in range(len(self.board)):  # number of rows
                    for c in range(len(self.board[r])):
                        if self.is_piece_of_right_turn(r, c):
                            self.get_piece_moves(r, c, second_move_list, first_move)

                for second_move in second_move_list:
                    move_list.append([first_move, second_move])

                self.simulate_undo_move(first_move)
                #self.turn -= 1

        return move_list

        #for moves in move_list:
        #    if len(moves) == 2:
        #        for i, check_moves in enumerate(move_list):
        #            if len(check_moves) == 2 and (moves[0].ID == check_moves[1].ID and moves[1].ID == check_moves[0].ID):
        #                move_list.pop(i)
        #                break
        #                #print(moves[0].ID + " " + moves[1].ID)
        #                #print(check_moves[0].ID + " " + check_moves[1].ID)
                #for smart_moves in smart_move_list:
                #    if asd


    def simulate_make_move(self, move): #change only the board
        if move.ID != "skip":
            self.board[move.start_r][move.start_c] = V
            self.board[move.end_r][move.end_c] = move.piece_moved

        self.update_turn(move)
        return move.ID



    def simulate_undo_move(self, last_move):
        if last_move.ID != "skip":
            self.board[last_move.start_r][last_move.start_c] = last_move.piece_moved
            self.board[last_move.end_r][last_move.end_c] = last_move.piece_captured

        self.reset_turn(last_move)

    def get_piece_moves(self, r, c, moves, last_move = None):
        if not last_move and len(self.game_log)>0:
            last_move = self.game_log[-1]

        if last_move:
            fm_r, fm_c = last_move.get_end_pos()
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
                    if endPiece == V:
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
        enemy_color = 0 if self.is_gold_turn() else 1 # pair if silver
        for d in directions:
            end_r = r + d[0]
            end_c = c + d[1]
            if 0 <= end_r < len(self.board) and 0 <= end_c < len(self.board):
                #endPiece = self.board[end_r][end_c]
                if self.is_valid_piece(end_r, end_c) and self.board[end_r][end_c]%2 == enemy_color:
                    move = Move((r, c), (end_r, end_c), self.board)
                    moves.append(move)


    def check_single_piece_moves(self, r, c): #subset of self.valid_moves
        move_list, capture_list = [], []
        for move in self.valid_moves:
            if move.start_r == r and move.start_c == c:
                if move.piece_captured:
                    capture_list.append(move)
                else:
                    move_list.append(move)
        return move_list, capture_list


    def check_victory(self):
        flagship_escaped = False
        flagship_killed = True

        # vertical check
        for i in range(len(self.board)):
            if self.board[i][0] == F or self.board[i][len(self.board)-1] == F:
                flagship_escaped = True

        # horizontal check
        for j in range(len(self.board[0])):
            if self.board[0][j] == F or self.board[len(self.board[0])-1][j] == F:
                flagship_escaped = True

        # kill check
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == F:
                    flagship_killed = False

        if flagship_escaped:
            return "GOLD_WIN"
        if flagship_killed:
            return "SILVER_WIN"
        return "GAME"


    def print_board(self, board = None):

        if not board:
            board = self.board

        string = ""
        for i in range(len(board)):
            for j in range(len(board[i])):
                string += str(board[i][j]) + "  "
            print(string + "\n")
            string = ""

        print("\n")

########################################################################################################################
########################################################################################################################
##############################   AI   ##################################################################################


    def init_ai(self, behaviour):
        self.ai_behaviour = behaviour


    def ai_choose_move(self, move_list):
        start_clock = pygame.time.get_ticks()
        move = None
        #if self.ai_behaviour == "THE_ALPHABETA_GUY":
        move, score = self.alphabeta_behaviour(move_list, 1)
        #elif self.ai_behaviour == "THE_NOMNOM_GUY":
        #    move = self.smart_nomnom_behaviour(move_list)

        end_clock = pygame.time.get_ticks()
        self.ai_timer += end_clock - start_clock
        return move, score


    def smart_nomnom_behaviour(self, move_list):
        print(self.evaluation_function(1,1,1))
        seed(datetime.now())

        nomnom_list = []
        for move in move_list:
            if move.is_capture_move():
                if move.is_capture_flag():
                    return move
                nomnom_list.append(move)

        for move in move_list:
            if move.piece_moved == F:
                if move.end_r == 0 or move.end_r == len(self.board)-1 or move.end_c == 0 or move.end_c == len(self.board[0]) - 1:
                    return move

        if len(nomnom_list) != 0:
            i = randint(0, len(nomnom_list) - 1)
            return nomnom_list[i]
        elif len(move_list) != 0:
            i = randint(0, len(move_list) - 1)
            return move_list[i]
        else:
            return None


    def alphabeta_behaviour(self, move_list, max_depth):
        max_turn = self.is_gold_turn()
        #node_number = 0

        next_move, eval_score = self.alphabeta_method(max_depth, max_turn, -INFINITE, INFINITE)
        #print(eval_score)
        return next_move, eval_score #move_list[selected_key_action]


    def alphabeta_method(self, current_depth, is_max_turn, alpha, beta):

        if current_depth == 0 or self.check_victory() != "GAME":
            return None, self.evaluation_function(1, 1, 1) #TODO
        #node_number += 1

        possible_moves =  self.get_all_possible_moves_AI()

        score = -INFINITE if is_max_turn else INFINITE
        move_target = None
        for moves in possible_moves:
            for move in moves:
                self.simulate_make_move(move)

            action_child, new_score = self.alphabeta_method(current_depth-1, not is_max_turn, alpha, beta)
            #print(action_child)
            #print(new_score)
            for move in moves:
                self.simulate_undo_move(move)

            if is_max_turn and new_score > score:
                move_target = moves
                score = new_score
                alpha = max(alpha, score)
                if alpha >= beta:
                    break

            elif (not is_max_turn) and new_score < score:
                move_target = moves
                score = new_score
                beta = min(beta, score)
                if alpha >= beta:
                    break

        return move_target, score


    def evaluation_function(self, A, B, C):
        evaluation = 0

        # check victory
        if self.is_flag_escaped(): #WIN GOLD
            return INFINITE

        pieces = self.get_number_of_ships()
        if pieces[0] == 0: #WIN SILVER
            return -INFINITE

        # number or pieces for both sides
        evaluation += A*pieces[1] - B*pieces[2]

        # distance_flag_from_edges
        #distance_flag = self.distance_flag_from_edges()
        #evaluation += C*(5-distance_flag[0]) + C*(5-distance_flag[1])


        whole_list = self.get_all_possible_moves()
        move_list = []
        capture_list = []
        capture_flag_list = []
        for move in whole_list:
            if move.is_capture_move():
                if move.is_capture_flag():
                    capture_flag_list.append(move)
                else:
                    capture_list.append(move)
            else:
                move_list.append(move)

        # number of legal moves
        evaluation += len(move_list) + 2*len(capture_list) - 10*len(capture_flag_list)
        # TODO

        # number of available captures
        # TODO

        # number of escape ways
        # TODO


        return evaluation


##############################   AI   ##################################################################################
########################################################################################################################
########################################################################################################################
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
    0:"a", 1:"b",
    2:"c", 3:"d",
    4:"e", 5:"f",
    6:"g", 7:"h",
    8:"i", 9:"j",
    10:"k"
}

class Move():

    def __init__(self, start_sq, end_sq, board):
        self.start_r = start_sq[0]
        self.start_c = start_sq[1]
        self.end_r = end_sq[0]
        self.end_c = end_sq[1]
        self.piece_moved = board[self.start_r][self.start_c]
        self.piece_captured = board[self.end_r][self.end_c]
        self.cost = 2 if (self.piece_captured or self.piece_moved == F) else 1
        self.ID = self.get_chess_notation()


    def init_skip_move(self): #SKIP MOVE
        self.start_r        = None
        self.start_c        = None
        self.end_r          = None
        self.end_c          = None
        self.piece_moved    = V
        self.piece_captured = V
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
        return cols_to_files[col] + rows_to_ranks[row]


    def is_capture_move(self):
        return True if self.piece_captured != V else False


    def is_capture_flag(self):
        return True if self.piece_captured == F else False
