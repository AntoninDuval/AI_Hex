import numpy as np
import gym
from gym import spaces
from application import GUI
from player import Human, Random_AI
from collections import namedtuple
import random

from mcts import Node, MCTS
from hex_board import HexBoard

class Hexagone(gym.Env):

    def __init__(self, render=True):


        #self.players = [Human(i) for i in range(1, 3)]
        self.players = [Human(1), Random_AI(2)]
        self.current_player = self.players[0]
        self.render = render


        self.action_space = spaces.Discrete(121)
        self.done = False
        self.reward = 0

        self.board = HexBoard(grille=np.zeros((11, 11)), current_player=self.current_player, players=self.players, winner=None, done=self.done)

        if self.render:
            self.gui = GUI(self)
            self.gui.mainloop()


    def step(self, event=None, coord=None):

        if self.gui is not None and self.current_player.type == 'human':
            coord = self.gui.get_hexagone(event)

        else:
            coord = self.current_player.move(self.board.grille)

        self.board = self.board.make_move(coord)

        self.gui.redraw_hex(coord, self.current_player)

        #self.reward = self.board.reward()

        if self.current_player.number == 1:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

        if self.current_player.type == 'ai':
            self.step()

        return self.board, self.reward, self.done

    def reset(self):

        self.board = HexBoard(grille=np.zeros((11, 11)), current_player=self.current_player, players=self.players, winner=None, done=self.done)
        if self.gui:
            self.gui.restart_app()




