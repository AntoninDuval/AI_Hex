from abc import ABC
import numpy as np
import random

from mcts import MCTS, Node

class Player(ABC):
    def __init__(self, type, number):
        self.type = type
        self.number = number
        self.name = self.type + " " + str(self.number)

    def move(self, grille):
        pass

class Human(Player):
    def __init__(self, number):
        super().__init__('human', number)


class Random_AI(Player):
    def __init__(self, number):
        super().__init__('ai', number)

    def move(self, grille):
        required = np.where(grille == 0)
        choice = random.randint(0, len(required[0]))
        coord = (required[0][choice], required[1][choice])
        return coord


class Strong_AI(Player):
    def __init__(self, number):
        super().__init__('ai', number)

    def move(self, grille):
        required = np.where(grille == 0)


