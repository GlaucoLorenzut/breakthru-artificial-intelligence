import pygame
from random import seed
from random import randint
from datetime import datetime


# logic of turn
G_1 = 0
G_2 = 1
S_1 = 2
S_2 = 3

# logic of pieces

V = 0  # VOID
G = 1  # GOLD ship
S = 2  # SILVER ship
F = 3  # FLAG

ROW_NOTATION = {
    0: "11", 1: "10", 2: "9", 3: "8", 4: "7", 5: "6", 6: "5", 7: "4", 8: "3", 9: "2", 10: "1"}

COLUMN_ROTATION = {
    0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j", 10: "k"}

INFINITE = 100000
AB_WNDW = 10000
MAX_TIME = 15000 #msec
RANDOM_MATRIX = [[[randint(0, 2**64 - 1) for i in range(3)] for j in range(11)] for k in range(11)] # TODO 0 or 1

EXACT = 0
LOWERBOUND = -1
UPPERBOUND = 1


class GameEngine():

    def __init__(self, ai_behaviour=None):

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
        #self.board = [
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, G, F, 0, 0, 0, 0, 0, 0],
        #    [0, S, 0, S, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #]
        #self.board = [
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, F, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #]

        self.turn = G_1
        self.game_log = []
        self.restore_log = []
        self.is_first_move = True
        self.valid_moves = self.get_all_possible_moves()
        self.ai_behaviour = ai_behaviour
        self.ai_timer = 0
        self.ai_time_calculation = 0
        self.ai_deep = 3
        self.node_searched = 0
        self.transposition_table = []


    ####################################################################################################################
    ################################################# LOGIC FUNCTIONS ##################################################
    ####################################################################################################################

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
        flag_pos = None

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == G:
                    n_gold_ship += 1
                elif self.board[i][j] == S:
                    n_silver_ship += 1
                elif self.board[i][j] == F:
                    n_gold_flag = 1
                    flag_pos = [i, j]

        return (n_gold_flag, n_gold_ship, n_silver_ship), flag_pos


    def distance_flag_from_edges(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == F:
                    y = min(i, len(self.board)-i-1)
                    x = min(j, len(self.board[0]) - j - 1)

        return (x, y)


    ####################################################################################################################
    ################################################# ACTIVE FUNCTIONS #################################################
    ####################################################################################################################

    def update_turn(self, move):
        self.turn = (self.turn + move.cost) % 4
        self.is_first_move = False


    def reset_turn(self, move):
        self.turn = (self.turn - move.cost) % 4


    def make_move_trial(self, move): #change only the board
        if move.ID != "skip":
            self.board[move.start[0]][move.start[1]] = V
            self.board[move.end[0]][move.end[1]] = move.piece_moved
        self.update_turn(move)
        return move.ID


    def make_move(self, move):
        self.make_move_trial(move)

        self.game_log.append(move)
        self.restore_log = []

        self.update_all_possible_moves()
        return move.ID


    def skip_move(self):
        skip = Move((1, 1), (1, 1), self.board)
        skip.init_skip_move()
        self.game_log.append(skip)
        self.update_turn(skip)
        self.restore_log = []

        self.update_all_possible_moves()
        return skip.ID


    def undo_move_trial(self, last_move):
        if last_move.ID != "skip":
            self.board[last_move.start[0]][last_move.start[1]] = last_move.piece_moved
            self.board[last_move.end[0]][last_move.end[1]] = last_move.piece_captured
        self.reset_turn(last_move)


    def undo_move(self):
        if len(self.game_log) > 0:
            last_move = self.game_log.pop()  # take and remove in one passage
            self.undo_move_trial(last_move)

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
                self.board[restore_move.start[0]][restore_move.start[1]] = V
                self.board[restore_move.end[0]][restore_move.end[1]] = restore_move.piece_moved
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
            for i in range(1, len(self.board)):
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
                if self.is_valid_piece(end_r, end_c) and self.board[end_r][end_c]%2 == enemy_color:
                    move = Move((r, c), (end_r, end_c), self.board)
                    moves.append(move)


    def check_single_piece_moves(self, r, c): #subset of self.valid_moves
        move_list, capture_list = [], []
        for move in self.valid_moves:
            if move.start[0] == r and move.start[1] == c:
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
############################################## AI FUNCTIONS ############################################################
########################################################################################################################

    def ai_choose_move(self):
        start_clock = pygame.time.get_ticks()
        self.ai_time_calculation = pygame.time.get_ticks()
        self.node_searched = 0
        move, score = self.alphabeta_minimax_method(self.ai_deep, self.is_gold_turn(), -AB_WNDW, AB_WNDW)

        self.ai_timer += pygame.time.get_ticks() - start_clock

        print("Tot node searched [ " + str(self.node_searched) + " ] in millis [ " + str(pygame.time.get_ticks() - start_clock) + " ]")
        return move, score


    def order_moves(self, move_list, is_max_turn):
        score_list = []
        for move in move_list:
            self.make_move_trial(move)
            score_list.append(self.evaluation_function(None))
            self.undo_move_trial(move)
        sorted_moves = list(zip(move_list, score_list))
        sorted_moves.sort(reverse=is_max_turn, key=lambda x: x[1])
        return [value[0] for value in sorted_moves]


    def get_zoobrist_hash(self):
        hash = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]:
                    piece_map = self.board[i][j] - 1
                    hash ^= RANDOM_MATRIX[i][j][piece_map]
        return hash


    def retrieve_status_from_hash(self):
        current_hash = self.get_zoobrist_hash()
        for node in self.transposition_table:
            if node.hash == current_hash:
                return node
        return None


    def store_node_in_tt(self, best_move, best_score, current_flag, current_depth):
        current_hash = self.get_zoobrist_hash()
        for i, node in enumerate(self.transposition_table): #NEW replacement scheme
            if node.hash == current_hash:
                self.transposition_table.pop(i)
                break
        self.transposition_table.append(Node(current_hash, best_move, best_score, current_flag, current_depth))


    def alphabeta_minimax_method(self, current_depth, is_max_turn, alpha, beta):
        self.node_searched += 1

        OLDA = alpha
        node = self.retrieve_status_from_hash()
        if node and node.depth >= current_depth:
            if node.flag == EXACT:
                #print("SERVE TT")
                return node.best_move, node.best_value
            elif node.flag == LOWERBOUND:
                alpha = max(alpha, node.best_value)
            else: #UPPERBOUND
                beta = min(beta, node.best_value)
            if alpha >= beta:
                #print("SERVE TT")
                return node.best_move, node.best_value

        game_status = self.check_victory()
        if current_depth == 0 or pygame.time.get_ticks() - self.ai_time_calculation > MAX_TIME or game_status != "GAME":
            return None, self.evaluation_function(game_status)

        next_moves = self.get_all_possible_moves()

        # next_moves = self.order_moves(next_moves, is_max_turn)

        best_score = -INFINITE if is_max_turn else INFINITE
        best_move = None
        for move in next_moves:
            self.make_move_trial(move) # updates also the turn
            max_turn = self.is_gold_turn()
            action_child, new_score = self.alphabeta_minimax_method(current_depth-1, max_turn, alpha, beta)
            self.undo_move_trial(move)

            if is_max_turn and new_score > best_score:
                best_move = move
                best_score = new_score
                alpha = max(alpha, new_score)
                if alpha >= beta:
                    break
            elif (not is_max_turn) and new_score < best_score:
                best_move = move
                best_score = new_score
                beta = min(beta, new_score)
                if alpha >= beta:
                    break

        # storing node on TT
        current_flag = EXACT
        if best_score <= OLDA:
            current_flag = UPPERBOUND
        elif best_score >= beta:
            current_flag = LOWERBOUND


        self.store_node_in_tt(best_move, best_score, current_flag, current_depth)

        #move_target_id = move_target.ID if move_target else "null"
        #print("DEP { " + str(current_depth) + " } MOVE { " + move_target_id + " } SCORE { " + str(best_score) +" }")
        return best_move, best_score


    def evaluation_function(self, status):
        evaluation = 0

        pieces, flag_pos = self.get_number_of_ships()

        #if status:
        if status == "GOLD_WIN":
            return AB_WNDW
        elif status == "SILVER_WIN":
            return -AB_WNDW
        #else:
        #    # check victory
        #    if self.is_flag_escaped(): #WIN GOLD
        #        return AB_WNDW
#
        #    #print(pieces[0])
        #    if pieces[0] == 0: #WIN SILVER
        #        return -AB_WNDW
#
        # number or pieces for both sides
        evaluation += 5*pieces[1] - 3*pieces[2]


        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        flag_under_attack = 0
        for d in directions:
            r = flag_pos[0] + d[0]
            c = flag_pos[1] + d[1]
            if self.board[r][c] == S:
                flag_under_attack += 1

        evaluation += (-200 * flag_under_attack)

        # number of escape ways
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        escape_ways = 0
        for d in directions:
            for i in range(1, len(self.board)):
                r = flag_pos[0] + d[0] * i
                c = flag_pos[1] + d[1] * i

                if 0 <= r < len(self.board) and 0 <= c < len(self.board):
                    next_square = self.board[r][c]
                    if next_square != V:
                        break
                    if r == 0 or r == len(self.board) - 1 or c == 0 or c == len(self.board[0]) - 1:
                        escape_ways += 1
                        break

        evaluation += 200 * escape_ways

        # TODO CHECK
        # distance_flag_from_edges
        #distance_flag = self.distance_flag_from_edges()
        #evaluation += C*(5-distance_flag[0]) + C*(5-distance_flag[1])

        #move_list = []
        #capture_list = []
        #capture_flag_list = []
        #for move in all_moves:
        #    if move.is_capture_move():
        #        if move.is_capture_flag():
        #            capture_flag_list.append(move)
        #        else:
        #            capture_list.append(move)
        #    else:
        #        move_list.append(move)

        # number of legal moves and number of available captures
        #evaluation += 0.5*len(move_list) + 1*len(capture_list) - 10*len(capture_flag_list)

        # number of flag eaten
        #flag_eaten_counter = 0
        #for move in capture_list:
        #    if move.piece_captured == F:
        #        evaluation += 1
        #evaluation += (-500*flag_eaten_counter)
#
        ## number of escape ways
        #escape_ways_counter = 0
        #for move in move_list:
        #    if move.piece_moved == F:
        #        if move.end[0] == 0 or move.end[0] == len(self.board) - 1 or move.end[1] == 0 or move.end[1] == len(self.board[0]) - 1:
        #            escape_ways_counter +=1
#
        #if escape_ways_counter == 3 or (escape_ways_counter == 3 and self.turn==S_2):
        #    return AB_WNDW
#
        #evaluation += 50*escape_ways_counter

        return evaluation

########################################################################################################################
############################################## TRANSPOSITION TABLE #####################################################
########################################################################################################################

class Move():

    def __init__(self, start_sq, end_sq, board):
        self.start = start_sq
        self.end = end_sq
        self.piece_moved = board[self.start[0]][self.start[1]]
        self.piece_captured = board[self.end[0]][self.end[1]]
        self.cost = 2 if (self.piece_captured or self.piece_moved == F) else 1
        self.ID = self.get_chess_notation()


    def init_skip_move(self): #SKIP MOVE
        self.start          = (None, None)
        self.end            = (None, None)
        self.piece_moved    = V
        self.piece_captured = V
        self.cost = 2
        self.ID = "skip"


    def __eq__(self, other): # overriding ==
        if isinstance(other, Move):
            return self.ID == other.ID
        return False


    def get_start_pos(self):
        return self.start


    def get_end_pos(self):
        return self.end


    def get_chess_notation(self):
        return COLUMN_ROTATION[self.start[1]] + ROW_NOTATION[self.start[0]] + "-" + COLUMN_ROTATION[self.end[1]] + ROW_NOTATION[self.end[0]]


    def is_capture_move(self):
        return True if self.piece_captured != V else False


    def is_capture_flag(self):
        return True if self.piece_captured == F else False



class Node():

    def __init__(self, hash, best_move, best_value, flag, depth):
        self.hash = hash
        self.best_move = best_move
        self.best_value = best_value
        self.flag = flag
        self.depth = depth
