from tkinter import *
from square import *
from piece import *
from color import *
from force import *

class Board(Frame):

    def __init__(self, parent, listener):
        Frame.__init__(self, parent)

        self.listener = listener
        self.board = Frame(parent)
        self.board.pack(side = TOP, fill = BOTH, expand = True)

        rankThree = Frame(self.board)
        rankThree.pack(side = TOP, fill = BOTH, expand = True)

        rankTwo = Frame(self.board)
        rankTwo.pack(side = TOP, fill = BOTH, expand = True)

        rankOne = Frame(self.board)
        rankOne.pack(side = TOP, fill = BOTH, expand = True)

        self.leds = {}
        self.labels = {}
        self.forceLabels = {}

        self._createSquare(rankOne, Square.A1)
        self._createSquare(rankOne, Square.B1)
        self._createSquare(rankOne, Square.C1)

        self._createSquare(rankTwo, Square.A2)
        self._createSquare(rankTwo, Square.B2)
        self._createSquare(rankTwo, Square.C2)

        self._createSquare(rankThree, Square.A3)
        self._createSquare(rankThree, Square.B3)
        self._createSquare(rankThree, Square.C3)

    def _piece(self, piece: Piece, color: Color):
        pieces = {
            Piece.K: "♚" if color == Color.black else "♔",
            Piece.Q: "♛" if color == Color.black else "♕",
            Piece.R: "♜" if color == Color.black else "♖",
            Piece.B: "♝" if color == Color.black else "♗",
            Piece.N: "♞" if color == Color.black else "♘",
            Piece.P: "♟" if color == Color.black else "♙"
        }
        return pieces[piece]

    def _background(self, square: Square):
        return ("#%02x%02x%02x" % (0, 102, 0)) if square.value % 2 != 0 else ("#%02x%02x%02x" % (191, 170, 134))

    def _foreground(self, color: Color):
        return 'white' if color == Color.white else 'black'

    def _createSquare(self, parent: Frame, square: Square):

        bg = self._background(square)

        label = Label(parent, text = " ", bg = bg, font=("Courier", 66))
        label.pack(side = LEFT, expand = True, fill = BOTH)
        label.bind("<Button-1>", lambda e: self._squareClicked(square))
        self.labels[square] = label

        forceLabel = Label(label, text = Force.neutral.value, bg = bg)
        forceLabel.place(relx=0.5, rely = 1.0, y = -2, anchor = S)
        self.forceLabels[square] = forceLabel

        led = Label(label, text = "", fg = 'red', bg = bg)
        led.place(relx=0.1, rely = 0.1, y = -2, anchor = N)
        self.leds[square] = led

    def setForce(self, square: Square, force: Force):
        self.forceLabels[square].configure(text = force.value)

    def attackable(self, isAttackable: bool, square: Square):
        self.leds[square].configure(text = "◉" if isAttackable else "")

    def mark(self, square: Square):
        self.labels[square].configure(bg = ("#%02x%02x%02x" % (0, 64, 255)))
        self.forceLabels[square].configure(bg = ("#%02x%02x%02x" % (0, 64, 255)))
        self.leds[square].configure(bg = ("#%02x%02x%02x" % (0, 64, 255)))

    def demark(self, square: Square):
        self.labels[square].configure(bg = self._background(square))
        self.forceLabels[square].configure(bg = self._background(square))
        self.leds[square].configure(bg = self._background(square))

    def _squareClicked(self, square):
        self.listener.board_clicked(square)

    def place(self, piece: Piece, color: Color, square: Square):
        fg = self._foreground(color)
        p = self._piece(piece, color)
        self.labels[square].config(text = p, fg = fg)
   
    def clear(self, square: Square):
        self.labels[square].config(text = " ")

    def clearAll(self):
        for square in Square:
            self.clear(square)
            self.demark(square)
