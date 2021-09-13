import tkinter as tk
import numpy as np
from src.utils import *

WIDTH, HEIGHT = 420, 225
DIM_HEX = 25
w = math.sqrt(3) * DIM_HEX

NB_COL = 11
NB_ROW = 11


class GUI(tk.Tk):
    def __init__(self, hex_sim, size, is_ai=False):
        self.hex_sim = hex_sim
        tk.Tk.__init__(self)
        self.title("Hex")
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="IVORY")
        self.canvas.pack(padx=5, pady=5)
        self.restart = tk.Button(self, text='Restart', command=self.hex_sim.reset)
        self.restart.pack(side=tk.BOTTOM, pady=5)
        self.canvas.bind("<Button-1>", self.hex_sim.step)
        self.is_ai = is_ai
        self.size_grid = size
        self.create_hexagones()

    def create_hexagones(self):
        self.center_array = np.ndarray((self.size_grid, self.size_grid, 2))
        for j in range(self.size_grid):
            for i in range(self.size_grid):
                self.canvas.create_polygon(5 + DIM_HEX / 2 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX / 4 + (j * 0.75 * DIM_HEX),
                                           5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                           5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                           5 + DIM_HEX * (i + 0.5) + (j * DIM_HEX / 2), 1.25 * DIM_HEX + (j * 0.75 * DIM_HEX),
                                           5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                           5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                           fill='white',
                                           outline='black',
                                           activefill='grey')
                if j == 0:
                    self.canvas.create_line(5 + DIM_HEX / 2 + (i * DIM_HEX), DIM_HEX / 4,
                                            5 + (i * DIM_HEX), DIM_HEX / 2,
                                            fill='red',
                                            width=2)

                    self.canvas.create_line(5 + DIM_HEX / 2 + (i * DIM_HEX), DIM_HEX / 4,
                                            5 + (i + 1) * DIM_HEX, DIM_HEX / 2,
                                            fill='red',
                                            width=2)
                if j == self.size_grid-1:
                    self.canvas.create_line(5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                            5 + DIM_HEX * (i + 0.5) + (j * DIM_HEX / 2), 1.25 * DIM_HEX + (j * 0.75 * DIM_HEX),
                                            fill='red',
                                            width=2)

                    self.canvas.create_line(5 + DIM_HEX * (i + 0.5) + (j * DIM_HEX / 2), 1.25 * DIM_HEX + (j * 0.75 * DIM_HEX),
                                           5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                            fill='red',
                                            width=2)

                if i == 0:
                    self.canvas.create_line(5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                           5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                            fill='blue',
                                            width=2)

                    self.canvas.create_line(5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                           5 + DIM_HEX * (i + 0.5) + (j * DIM_HEX / 2), 1.25 * DIM_HEX + (j * 0.75 * DIM_HEX),
                                            fill='blue',
                                            width=2)
                if i == self.size_grid-1:

                    self.canvas.create_line(5 + DIM_HEX / 2 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX / 4 + (j * 0.75 * DIM_HEX),
                                            5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                            fill='blue',
                                            width=2)

                    self.canvas.create_line(5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                           5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                            fill='blue',
                                            width=2)

                self.center_array[i, j] = np.array(
                    [DIM_HEX * (i + 0.5) + (j * DIM_HEX / 2), 0.5 * DIM_HEX + (j * 0.75 * DIM_HEX)])

    def get_hexagone(self, event):
        pos_x = event.x - 5
        pos_y = event.y - DIM_HEX/4

        min_dist = np.linalg.norm(self.center_array[0, 0] - [pos_x, pos_y])
        coord = (0, 0)
        for j in range(self.size_grid):
            for i in range(self.size_grid):
                dist = np.linalg.norm(self.center_array[i, j]-[pos_x, pos_y])
                if dist < min_dist:
                    min_dist = dist
                    coord = (i, j)

        return coord

    def redraw_hex(self, coord, player):

        i, j = coord[0], coord[1]

        if player.number == 1:
            COLOR = 'red'
        else:
            COLOR = 'blue'

        self.canvas.create_polygon(5 + DIM_HEX / 2 + (i * DIM_HEX) + (j * DIM_HEX / 2),
                                   DIM_HEX / 4 + (j * 0.75 * DIM_HEX),
                                   5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                   5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                   5 + DIM_HEX * (i + 0.5) + (j * DIM_HEX / 2), 1.25 * DIM_HEX + (j * 0.75 * DIM_HEX),
                                   5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                   5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2),
                                   DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                   fill=COLOR,
                                   outline='black')

    def restart_app(self):
        self.canvas.delete(tk.ALL)
        self.create_hexagones()












