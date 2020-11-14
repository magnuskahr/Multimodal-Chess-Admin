
from board_controller import *
from servo_controller import *

from square import *

class Controller():

    def __init__(self):

        self.board: BoardController = None
        self.servo: ServoController = None

        self.lifting = None

        return

    def board_lifted_square(self, square: Square):
        _, color, piece = self.board.get(square)
        print("lifting " + piece + " of color " + color + " from " + square)
        self._lift(color, piece, square)
        return

    def board_placed_square(self, square: Square):
        if self.lifting == None: return
        print("placed " + self.lifting["piece"] + " on " + square)
        self._place(square)

    def setForce(self, a, b):
        return
        
    def _lift(self, color, piece, fromSquare):
        self.lifting = {
            "color": color,
            "piece": piece,
            "square": fromSquare
        }

    def _place(self, onSquare):
        self.lifting = None