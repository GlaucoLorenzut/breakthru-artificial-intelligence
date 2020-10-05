
from random import seed
from random import randint
from datetime import datetime
import pygame
import game_engine
import time

INFINITE = 1000000000

class AI():

    def __init__(self, board, behaviour=None):
        self.board = board
        self.behaviour = behaviour
        self.timer = 0


    def init_ai(self, behaviour):
        self.behaviour = behaviour


    def choose_move(self, move_list):
        start_clock = pygame.time.get_ticks()
        move = None
        if self.behaviour == "THE_ALPHABETA_GUY":
            move = self.alphabeta_behaviour(move_list)
        elif self.behaviour == "THE_NOMNOM_GUY":
            move = self.smart_nomnom_behaviour(move_list)
        elif self.behaviour == "THE_RANDOM_GUY":
            move = self.random_behaviour(move_list)

        #time.sleep(0.30)
        end_clock = pygame.time.get_ticks()
        self.timer += end_clock - start_clock
        #print("s:[" + str(start_clock) + "]  e:[" + str(end_clock) + "]  T:[" + str(self.timer) + "]")
        return move


    def random_behaviour(self, move_list):
        print(self.distance_flag_from_edges())
        seed(datetime.now())
        if len(move_list) != 0:
            i = randint(0, len(move_list) - 1)
            return move_list[i]
        else:
            return None

    def nomnom_behaviour(self, move_list):
        seed(datetime.now())

        nomnom_list = []
        for move in move_list:
            if move.is_capture_move():
                nomnom_list.append(move)

        if len(nomnom_list) != 0:
            i = randint(0, len(nomnom_list) - 1)
            return nomnom_list[i]
        elif len(move_list) != 0:
            i = randint(0, len(move_list) - 1)
            return move_list[i]
        else:
            return None

    def smart_nomnom_behaviour(self, move_list):
        seed(datetime.now())

        nomnom_list = []
        for move in move_list:
            if move.is_capture_move():
                if move.is_capture_flag():
                    return move
                nomnom_list.append(move)

        for move in move_list:
            if move.piece_moved == "gF":
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


    def alphabeta_behaviour(self, move_list):
        # ciccio = alphabeta(self, state, depth, -INFINITE, INFINITE):
        pass


    def alphabeta(self, state, depth, alpha, beta):
        pass
        #if terminal_node or depth == 0:
        #    return evaluation_fucntion(state)
        #score = -INFINITE


    def evaluation_function(self, A, B, C):
        evaluation = 0

        # check victory
        if self.is_flag_escaped(): #WIN GOLD
            return INFINITE

        pieces = self. get_number_of_ships()
        if pieces[0] == 0: #WIN SILVER
            return -INFINITE

        # number or pieces for both sides
        evaluation += A*pieces[1] - B*pieces[2]

        # distance_flag_from_edges
        distance_flag = self.distance_flag_from_edges()
        evaluation += C*(5-distance_flag[0]) + C*(5-distance_flag[1])

        # number of legal moves
        move_list = get

        # TODO

        # number of available captures
        # TODO

        # number of escape ways
        # TODO


        return evaluation



    def is_flag_escaped(self):
        flagship_escaped = False

        # vertical check
        for i in range(len(self.board)):
            if self.board[i][0] == "gF" or self.board[i][len(self.board)-1] == "gF":
                flagship_escaped = True

        # horizontal check
        for j in range(len(self.board[0])):
            if self.board[0][j] == "gF" or self.board[len(self.board[0])-1][j] == "gF":
                flagship_escaped = True

        return flagship_escaped


    def get_number_of_ships(self):
        n_gold_flag, n_gold_ship, n_silver_ship = 0, 0, 0

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j][0] == "g":
                    if self.board[i][j][1] == "S":
                        n_gold_ship += 1
                    else:
                        n_gold_flag = 1
                elif self.board[i][j][0] == "s":
                    n_silver_ship += 1

        return (n_gold_flag, n_gold_ship, n_silver_ship)

    def distance_flag_from_edges(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == "gF":
                    y = min(i, len(self.board)-i-1)
                    x = min(j, len(self.board[0]) - j - 1)

        return (x, y)

