
from random import seed
from random import randint
# seed random number generator
seed(1)
# generate some integers
for _ in range(100):
	value = randint(0, 10)
	print(value)


class AI():
    def __init__(self, behaviour):
        self.behaviour = behaviour



    def choose_move(self, move_list):
        if self.behaviour == "THE_RANDOM_GUY":
            pass
        elif self.behaviour == "THE_NOMNOM_GUY":
            pass