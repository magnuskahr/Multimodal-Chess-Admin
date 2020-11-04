from square import *
from piece import *
from color import *
from force import *
import keyboard

class BoardController():

    def __init__(self):

        self.board = None
        self.selector = None

        self.selector_selected_piece = None
        self.selector_selected_color = None

        self.board_selected_square = None

        self.board_data = {
            Square.A1: None,
            Square.A2: None,
            Square.A3: None,

            Square.B1: None,
            Square.B2: None,
            Square.B3: None,

            Square.C1: None,
            Square.C2: None,
            Square.C3: None
        }
        
        keyboard.add_hotkey("space", lambda: self._keyPressed("space"))
        keyboard.add_hotkey("down", lambda: self._keyPressed("down"))
        keyboard.add_hotkey("up", lambda: self._keyPressed("up"))

    def _keyPressed(self, key):
        if (self.board_selected_square == None): return
 
        if (key == "space"):
            self.board.setForce(self.board_selected_square, Force.neutral)
        elif (key == "down"):
            self.board.setForce(self.board_selected_square, Force.pull)
        elif (key == "up"):
            self.board.setForce(self.board_selected_square, Force.push)
        else:
            return

        self.board.demark(self.board_selected_square)
        self.board_selected_square = None


    def selector_clicked(self, piece: Piece, color: Color):
        if (self.selector == None): return

        # if a square is marked on the board
        if (self.board_selected_square != None):
            self.board.demark(self.board_selected_square)
            self.place(piece, color, self.board_selected_square)
            self.board_selected_square = None
            return

        # if you mark another piece in the selector
        if (self.selector_selected_piece != None and self.selector_selected_color != None):
            self.selector.demark(self.selector_selected_piece, self.selector_selected_color)
        
        # demark if same selected again
        if (self.selector_selected_piece == piece and self.selector_selected_color == color):
            self.selector_selected_color = None
            self.selector_selected_piece = None
            self.selector.demark(self.selector_selected_piece, self.selector_selected_color)
            return

        self.selector_selected_color = color
        self.selector_selected_piece = piece
        self.selector.mark(piece, color)

    def board_clicked(self, square: Square):
        # if a piece is about to be placed
        if (self.selector_selected_piece != None and self.selector_selected_color != None):
            self.place(self.selector_selected_piece, self.selector_selected_color, square)
            self.selector.demark(self.selector_selected_piece, self.selector_selected_color)
            self.selector_selected_color = None
            self.selector_selected_piece = None
            return
        
        # if selecting a piece on the board to move, or moving selection
        if (self.board_selected_square == None):
            self.board_selected_square = square
            self.board.mark(square)
            return

         # if deselecting
        if (self.board_selected_square == square):
            self.board.demark(self.board_selected_square)
            self.board_selected_square = None

        # if moving selection
        if (not self.occupied(self.board_selected_square)):
            self.board.demark(self.board_selected_square)
            self.board.mark(square)
            self.board_selected_square = square
            return
        
        # if performing a move
        self.move(self.board_selected_square, square)
        self.board.demark(self.board_selected_square)
        self.board_selected_square = None

    def move(self, fromSquare: Square, toSquare: Square):
        occupied, color, piece = self.get(fromSquare)
        if (occupied == False): 
            return

        self.clear(fromSquare)
        self.place(piece, color, toSquare)

    def clear(self, square: Square):
        self.board_data[square] = None
        self.board.clear(square)

    def occupied(self, square: Square):
        o, _, _ = self.get(square)
        return o

    def get(self, square: Square):
        color = self.getColor(square)
        piece = self.getPiece(square)
        if (piece == None or color == None):
            return False, None, None
        else:
            return True, color, piece

    def getColor(self, square: Square):
        data = self.board_data[square]
        if (data == None):
            return None
        else: return data["color"]

    def getPiece(self, square: Square):
        data = self.board_data[square]
        if (data == None):
            return None
        else: return data["piece"]

    def place(self, piece: Piece, color: Color, square: Square):
        self.board.place(piece, color, square)
        self.board_data[square] = {
            "piece": piece,
            "color": color
        }

    def test(self):
        self.board.place(Piece.K, Color.black, Square.C3)
        self.board.place(Piece.R, Color.white, Square.B1)
        self.board.place(Piece.R, Color.white, Square.A2)

