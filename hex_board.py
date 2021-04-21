from collections import namedtuple
import random
import numpy as np

from mcts import Node, MCTS

_TTTB = namedtuple("TicTacToeBoard", "grille current_player players winner done")

class HexBoard(_TTTB, Node):

    def find_children(self):
        if self.done:
            return set()  # If the game is finished then no moves can be made
        return {
            self.make_move(i) for i in self.find_all_move()
        }

    def find_random_child(self):
        if self.done:
            return None
        required = self.find_all_move()
        choice = random.randint(0, len(required[0]))
        return self.make_move((required[0][choice], required[1][choice]))

    def find_all_move(self):
        required = np.where(self.grille == 0)
        return required

    def reward(self):
        if not self.done:
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if self.winner is self.current_player:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board {self}")
        if self.current_player is (not self.winner):
            return 0  # Your opponent has just won. Bad.
        if self.winner is None:
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {self.winner}")

    def is_terminal(self):
        return self.done

    def make_move(self, coord):
        if self.grille[coord] == 0:
            self.grille[coord] = self.current_player.number # We change the grid with the move made
        else: # Then illegal move, we return the same grid
            return HexBoard(self.grille, self.current_player, self.players,  self.winner, self.is_terminal())

        current_player = self.players[1] if self.current_player.number == 0 else self.players[0]
        winner = self.detect_victory()
        done = winner is not None
        return HexBoard(self.grille, current_player, self.players, winner, done)

    def detect_victory(self):
        '''
        Use Breadth first to find a path from one end to the other
        :return:
        '''
        queue = set()
        came_from = dict()

        for j in range(11):
            if self.current_player.number == 2:
                if int(self.grille[0, j]) == self.current_player.number:
                    queue.add((0, j))
                    came_from[(0, j)] = None

            else:
                if int(self.grille[j, 0]) == self.current_player.number:
                    queue.add((j, 0))
                    came_from[(j, 0)] = None

        while queue:
                current = queue.pop()
                for next in self.find_neighbors(current):
                    if next not in came_from.values():
                        queue.add(next)
                        came_from[next] = current

                    if (next[1] == 10 and self.current_player.number == 1) or \
                            (next[0] == 10 and self.current_player.number == 2): # Si un chemin mène jusquà la dernière case
                        print('Player {} win'.format(self.current_player.name))
                        return self.current_player
        return None

    def find_neighbors(self, node):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if self.grille[node[0]+i, node[1]+j] == self.current_player.number and not i == j == 0:
                        neighbors.append((node[0]+i, node[1]+j))
                except IndexError:
                    continue
        return neighbors