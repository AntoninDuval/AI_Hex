import numpy as np
import gym
from gym import spaces
from application import GUI
from player import Human, Random_AI, MCTS_Player

from src.hex_board import HexBoard

NB_COL = 11
NB_ROW = 11

class Hexagone(gym.Env):

    def __init__(self, render=True, ai_difficulty=None, size=11):

        if ai_difficulty == 'random':
            self.players = [Human(1), Random_AI(2)]
        elif ai_difficulty == 'MCTS':
            self.players = [Human(1), MCTS_Player(2)]
        else:
            self.players = [Human(1), Human(2)]

        self.current_player = self.players[0]
        self.render = render

        self.action_space = spaces.Discrete(121)
        self.done = False
        self.reward = 0
        self.size = size

        self.board = HexBoard(grille=np.zeros((size, size)),
                              current_player=self.current_player,
                              players=self.players,
                              winner=None,
                              done=self.done)

        if self.render:
            self.gui = GUI(self, size)
            self.gui.mainloop()


    def step(self, event=None, coord=None):

        if self.gui is not None and self.board.current_player.type == 'human':

            coord = self.gui.get_hexagone(event)
            # We check that we don't play a hexagon already played
            if self.board.grille[coord] != 0:
                return None

            self.board = self.board.make_move(coord)

        else: # If the player is an AI
            new_board = self.board.current_player.move(self.board)
            diff = np.where(new_board.grille - self.board.grille != 0)
            coord = (diff[0][0], diff[1][0])
            self.board = new_board

        if self.render: # Redraw the hexagones that was played to be the same color as the player
            self.gui.redraw_hex(coord, self.current_player)

        self.current_player = self.board.current_player

        if self.board.current_player.type == 'ai':
            self.step()

        return self.board, self.reward, self.done

    def reset(self):

        self.board = HexBoard(grille=np.zeros((self.size, self.size)),
                              current_player=self.players[0],
                              players=self.players,
                              winner=None,
                              done=self.done)
        self.current_player = self.board.current_player

        if self.gui:
            self.gui.restart_app()




