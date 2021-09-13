from collections import namedtuple
import random
import numpy as np
import copy
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
        all_moves = self.find_all_move()
        choice = random.choice(all_moves)
        return self.make_move(choice)

    def find_all_move(self):
        '''
        Return all possible move in this position
        :return:
        '''
        all_move = []
        required = np.where(self.grille == 0)
        for i in range(len(required[0])):
            all_move.append((required[0][i], required[1][i]))
        return all_move

    def reward(self):
        if not self.done:
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if self.winner is self.current_player.number:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board {self}")
        if self.current_player.number != self.winner and self.winner != 'Tie':
            return 0  # Your opponent has just won. Bad.
        if self.winner is None or self.winner == 'Tie':
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {self.winner}")

    def is_terminal(self):
        return self.done

    def make_move(self, coord):
        grille = copy.deepcopy(self.grille)
        if self.grille[coord] == 0:
            grille[coord] = self.current_player.number # We change the grid with the move made
        else:# Then illegal move, we return the same grid
            return HexBoard(grille, self.current_player, self.players,  self.winner, self.is_terminal())

        current_player = self.players[1] if self.current_player.number == 1 else self.players[0]
        winner = self.detect_victory(grille)
        done = winner is not None
        return HexBoard(grille, current_player, self.players, winner, done)

    def detect_victory(self, grille):
        '''
        Use Breadth first to find a path from one end to the other
        :return:
        '''
        queue = set()
        came_from = dict()

        last_col = grille.shape[0] - 1

        for j in range(grille.shape[0]):
            if self.current_player.number == 2:
                if int(grille[0, j]) == self.current_player.number:
                    # If one of the start hexagone for player 2 was played by him, we add it to the queue
                    queue.add((0, j))
                    came_from[(0, j)] = None
            else:
                if int(grille[j, 0]) == self.current_player.number:
                    queue.add((j, 0))
                    came_from[(j, 0)] = None

        while queue:
                current = queue.pop()
                for next in self.find_neighbors(current, grille):
                    if next not in came_from.values():
                        queue.add(next)
                        came_from[next] = current

                    if (next[1] == last_col and self.current_player.number == 1) or \
                            (next[0] == last_col and self.current_player.number == 2):
                        # Si un chemin mène jusquà la dernière case
                        print('Player {} win'.format(self.current_player.name))
                        return self.current_player.number

        if not grille.all() == 0:
            print('It\'s a Tie')
            return 'Tie'
        return None

    def detect_tie(self, grille):
        '''
        Use Breadth first to find a path from one end to the other
        :return:
        '''
        queue = set()
        came_from = dict()

        for j in range(self.grille.shape[0]):
            if self.current_player.number == 1:
                if int(grille[0, j]) == self.current_player.number:
                    # If one of the start hexagone for player 1 was played by him, we add it to the queue
                    queue.add((0, j))
                    came_from[(0, j)] = None
            else:
                if int(grille[j, 0]) == self.current_player.number:
                    queue.add((j, 0))
                    came_from[(j, 0)] = None

        while queue:
            current = queue.pop()
            for next in self.find_neighbors(current, grille):
                if next not in came_from.values():
                    queue.add(next)
                    came_from[next] = current

                if (next[1] == grille.shape[0] - 1 and self.current_player.number == 2) or \
                        (next[0] == grille.shape[0] - 1 and
                         self.current_player.number == 1):
                    # Si un chemin mène jusquà la dernière case
                    return True


    def find_neighbors(self, node, grille):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2): # We try every neighboring hexagones to see if they have been played
                try:
                    if grille[node[0]+i, node[1]+j] == self.current_player.number \
                            and not i == j == 0\
                            and node[0]+i != -1\
                            and node[1]+j != -1\
                            and not i == j == -1\
                            and not i == j == 1:
                        neighbors.append((node[0]+i, node[1]+j))
                        # Add it to the list of neighbors
                except IndexError:
                    continue
        return neighbors



    def __hash__(self):
        return hash(str(self.grille)+str(self.current_player))

    def __eq__(self, node2):
        return (self.grille == node2.grille).all()
