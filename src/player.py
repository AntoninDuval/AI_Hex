from abc import ABC
import numpy as np
import random
from datetime import datetime

from mcts import MCTS
from src.hex_board import HexBoard

class Player(ABC):
    def __init__(self, type, number):
        self.type = type
        self.number = number
        self.name = self.type + " " + str(self.number)

    def move(self, grille):
        pass

    def __eq__(self, other):
        try:
            return self.number == other.number
        except AttributeError:
            return False

class Human(Player):
    def __init__(self, number):
        super().__init__('human', number)


class Random_AI(Player):
    def __init__(self, number):
        super().__init__('ai', number)

    def move(self, board: HexBoard):
        required = np.where(board.grille == 0)
        choice = random.randrange(0, len(required[0]))
        coord = (required[0][choice], required[1][choice])
        board = board.make_move(coord)

        return board


class MCTS_Player(Player):
    def __init__(self, number):
        super().__init__('ai', number)
        self.tree = MCTS()

    def move(self, board):
        start_time = datetime.now()
        for _ in range(50):
            print(_)
            self.tree.do_rollout(board)
            delta = datetime.now() - start_time
            if delta.total_seconds() > 10:
                break
        board = self.tree.choose(board)
        return board


