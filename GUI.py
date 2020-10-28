from tkinter import *
from square import *
from piece import *
from color import *
from board import *
from piece_selector import *

class GUI:

   def __init__(self, board_controller):

      self.window = Tk(className = "Chess admin")
      self.window.geometry("500x800")

      self.board = Board(self.window, board_controller)
      self.board.pack(side = TOP, fill = BOTH, expand = True)
      board_controller.board = self.board

      self.pieceSelector = PieceSelector(self.window, board_controller)
      self.pieceSelector.pack(side = TOP, fill = BOTH, expand = True)
      board_controller.selector = self.pieceSelector

      controls = Frame(self.window, bg = "gray")
      controls.pack(side = BOTTOM, fill = BOTH, expand = True)

      button = Button(controls, text = "Test", command = self.test, bg = "black")
      button.pack()

   def test(self):
      self.board.clearAll()

      self.board.place(Piece.K, Color.white, Square.B2)

   def start(self):

      self.window.mainloop()