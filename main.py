import tkinter as tk
from application import Application
from hex import Hexagone


def main():
    hex_sim = Hexagone()
    app = Application(hex_sim)
    app.mainloop()



if __name__ == '__main__':
    main()