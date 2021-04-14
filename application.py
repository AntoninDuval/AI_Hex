import tkinter as tk
import numpy as np

WIDTH, HEIGHT = 775, 425
DIM_HEX = 47


class Application(tk.Tk):
    def __init__(self, hex_sim):
        tk.Tk.__init__(self)
        self.title("Hex")
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="IVORY")
        self.canvas.pack(padx=5, pady=5)
        self.create_hexagones()

        self.canvas.bind("<Button-1>", self.get_hexagone)

    def create_hexagones(self):
        for j in range(11):
            for i in range(11):
                self.canvas.create_polygon(5 + DIM_HEX / 2 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX / 4 + (j * 0.75 * DIM_HEX),
                                          5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                          5 + (i * DIM_HEX) + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                          5 + DIM_HEX * (i + 0.5) + (j * DIM_HEX / 2),
                                          1.25 * DIM_HEX + (j * 0.75 * DIM_HEX),
                                          5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX + (j * 0.75 * DIM_HEX),
                                          5 + (i + 1) * DIM_HEX + (j * DIM_HEX / 2), DIM_HEX / 2 + (j * 0.75 * DIM_HEX),
                                          fill='white',
                                          outline='black',
                                          activefill='grey')

    def get_hexagone(self, event):


        pos_x = event.x-5

        pos_y = event.y - 12.25

        print('x :', pos_x, 'y :', pos_y)

        print('x%47 :', pos_x%DIM_HEX , 'y%47:', pos_y%DIM_HEX)

        if (47-pos_x%DIM_HEX) < DIM_HEX/2 and 35.75 < pos_y%DIM_HEX < 47:
            print('POS Y = ', pos_y//DIM_HEX+1)
        else:
            print('POS Y = ', pos_y//DIM_HEX)




