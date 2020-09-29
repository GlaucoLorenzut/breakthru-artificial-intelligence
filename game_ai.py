
from random import seed
from random import randint
from datetime import datetime
import pygame
import game_engine


class AI():
    def __init__(self, behaviour):
        self.behaviour = behaviour
        self.timer = 0



    def choose_move(self, move_list):
        start_clock = pygame.time.get_ticks()
        move = None
        if self.behaviour == "THE_ALPHABETA_GUY":
            move = self.random_behaviour(move_list)
        elif self.behaviour == "THE_NOMNOM_GUY":
            move = self.nomnom_behaviour(move_list)
        elif self.behaviour == "THE_RANDOM_GUY":
            move = self.nomnom_behaviour(move_list)
        end_clock = pygame.time.get_ticks()
        self.timer += end_clock - start_clock
        print("s:[" + str(start_clock) + "]  e:[" + str(end_clock) + "]  T:[" + str(self.timer) + "]")
        return move

    def random_behaviour(self, move_list):
        seed(datetime.now())
        i = randint(0, len(move_list) - 1)
        return move_list[i]

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