
from random import seed
from random import randint
from datetime import datetime
import game_engine


class AI():
    def __init__(self, behaviour):
        self.behaviour = behaviour



    def choose_move(self, move_list):
        if self.behaviour == "THE_RANDOM_GUY":
            #list = self.game.valid_moves
            seed(datetime.now())
            i = randint(0, len(move_list) - 1)
            return move_list[i]

        elif self.behaviour == "THE_NOMNOM_GUY":
            seed(datetime.now())

            nomnom_list = []
            for move in  move_list:
                if move.piece_captured != "--":
                    nomnom_list.append(move)

            if len(nomnom_list) != 0:
                i = randint(0, len(nomnom_list) - 1)
                return nomnom_list[i]
            elif len(move_list) != 0:
                i = randint(0, len(move_list) - 1)
                return move_list[i]