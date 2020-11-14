
from board_controller import *
from servo_controller import *

from square import *
from color import *
from piece import *

class Controller():

    def __init__(self):

        self.board: BoardController = None
        self.servo: ServoController = None

        self.lifting = None

        return

    def board_lifted_square(self, square: Square):
        occupied, color, piece = self.board.get(square)
        if occupied == False:
            print("Error: lifted an onregistred piece from " + str(square))
            return

        if self.lifting != None:
            print("Lifted attacked piece")
            self.board.clear(square)
            return

        print("lifting " + str(piece) + " of color " + str(color) + " from " + str(square))
        self._lift(color, piece, square)
        return

    def board_placed_square(self, square: Square):
        if self.lifting == None: 
            
            occupied, color, piece = self.board.get(square)
            if occupied:
                # if we are placing piece on board from GUI
                print("placed the " + str(color) + " " + str(piece) + " on " + str(square))
            else:
                # if we are setting up the board frely
                print("placed a piece freely on " + str(square) + "")
            return

        # we are moving a piece    
        print("placed " + str(self.lifting["piece"]) + " on " + str(square))
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
        self.board.move(self.lifting["square"], onSquare)
        self.lifting = None