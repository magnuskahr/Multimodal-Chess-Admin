from tkinter import *
from square import *
from piece import *
from color import *
from board import *
from piece_selector import *
import json
import random

PUBLIC_ENUMS = {
    'Square': Square,
    'Color': Color,
    'Piece': Piece
}

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in PUBLIC_ENUMS.values():
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)

def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d

class GUI:

   def __init__(self, board_controller, mode):
      self.modal = mode
      self.boards = []
      try:
         with open('board_data.json', 'r') as openfile: 
            self.boards = json.load(openfile, object_hook=as_enum)
      except OSError:
         print('Well darn.')
      

      self.window = Tk(className = "Chess admin")
      self.window.geometry("500x800")

      self.board_controller = board_controller
      self.board = Board(self.window, board_controller)
      self.board.pack(side = TOP, fill = BOTH, expand = True)
      board_controller.board = self.board

      self.pieceSelector = PieceSelector(self.window, board_controller)
      self.pieceSelector.pack(side = TOP, fill = BOTH, expand = True)
      board_controller.selector = self.pieceSelector

      controls = Frame(self.window, bg = "gray")
      controls.pack(side = BOTTOM, fill = BOTH, expand = True)

      clearButton = Button(controls, text = "Clear", command = self.clear, bg = "white", fg = "black")
      clearButton.pack()

      saveButton = Button(controls, text = "Save", command = self.save, bg = "white", fg = "black")
      saveButton.pack()

      button1 = Button(controls, text = "puzzle 1", command = self.puzzle1, bg = "white", fg = "black")
      button1.pack()
      
      button2 = Button(controls, text = "puzzle 2", command = self.puzzle2, bg = "white", fg = "black")
      button2.pack()

   def clear(self):
      self.board_controller.reset()

   def save(self):
      converted = {
         'a1': self.board_controller.board_data[Square.A1],
         'b1': self.board_controller.board_data[Square.B1],
         'c1': self.board_controller.board_data[Square.C1],

         'a2': self.board_controller.board_data[Square.A2],
         'b2': self.board_controller.board_data[Square.B2],
         'c2': self.board_controller.board_data[Square.C2],

         'a3': self.board_controller.board_data[Square.A3],
         'b3': self.board_controller.board_data[Square.B3],
         'c3': self.board_controller.board_data[Square.C3]
      }
      self.boards.append(converted)
      data = json.dumps(self.boards, cls=EnumEncoder)
      
      with open("board_data.json", "w") as outfile: 
         outfile.write(data) 
   
   def puzzle1(self):
      def e(s):
         if s == "a1": return Square.A1
         if s == "a2": return Square.A2
         if s == "a3": return Square.A3
         if s == "b1": return Square.B1
         if s == "b2": return Square.B2
         if s == "b3": return Square.B3
         if s == "c1": return Square.C1
         if s == "c2": return Square.C2
         if s == "c3": return Square.C3


      self.board_controller.clearForces()

      randomBoard = self.get_board(self.modal, 1)
      
      for square in randomBoard:
         if randomBoard[square] != None:
            piece = randomBoard[square]['piece']
            color = randomBoard[square]['color']
            self.board_controller.place(piece, color, e(square))
         else:
            self.board_controller.clear(e(square))
            
   def puzzle2(self):
      def e(s):
         if s == "a1": return Square.A1
         if s == "a2": return Square.A2
         if s == "a3": return Square.A3
         if s == "b1": return Square.B1
         if s == "b2": return Square.B2
         if s == "b3": return Square.B3
         if s == "c1": return Square.C1
         if s == "c2": return Square.C2
         if s == "c3": return Square.C3
         
         
      self.board_controller.clearForces()
      
      randomBoard = self.get_board(self.modal, 2)
      
      for square in randomBoard:
         if randomBoard[square] != None:
            piece = randomBoard[square]['piece']
            color = randomBoard[square]['color']
            self.board_controller.place(piece, color, e(square))
         else:
            self.board_controller.clear(e(square))


   def start(self):
      #self.window.mainloop()
      self.window.update_idletasks()
      self.window.update()
      
   def get_board(self, modal, puzzle):
      if modal == "ingen":
         if puzzle == 1:
            return {
               'a1': None, 
               'b1': { 'piece': Piece.K, 'color': Color.black },
               'c1': None, 
               'a2': None, 
               'b2': None, 
               'c2': { 'piece': Piece.R, 'color': Color.white }, 
               'a3': { 'piece': Piece.B, 'color': Color.white }, 
               'b3': { 'piece': Piece.N, 'color': Color.white }, 
               'c3': { 'piece': Piece.R, 'color': Color.white }
            }
         if puzzle == 2:
            return {
               'a1': { 'piece': Piece.K, 'color': Color.black },
               'b1': None,
               'c1': { 'piece': Piece.B, 'color': Color.white }, 
               'a2': { 'piece': Piece.P, 'color': Color.white }, 
               'b2': None,
               'c2': { 'piece': Piece.B, 'color': Color.white }, 
               'a3': None, 
               'b3': None, 
               'c3': { 'piece': Piece.R, 'color': Color.white }
            }
      elif modal == "lys": 
         if puzzle == 1:
            return {
               'a1': { 'piece': Piece.K, 'color': Color.black }, 
               'b1': None,
               'c1': None, 
               'a2': { 'piece': Piece.P, 'color': Color.white },
               'b2': { 'piece': Piece.P, 'color': Color.white }, 
               'c2': { 'piece': Piece.Q, 'color': Color.white }, 
               'a3': None,
               'b3': None, 
               'c3': { 'piece': Piece.R, 'color': Color.white }
            }
         if puzzle == 2:
            return {
               'a1': None, 
               'b1': { 'piece': Piece.K, 'color': Color.black },
               'c1': None, 
               'a2': { 'piece': Piece.P, 'color': Color.white }, 
               'b2': { 'piece': Piece.P, 'color': Color.white }, 
               'c2': None, 
               'a3': { 'piece': Piece.R, 'color': Color.white }, 
               'b3': { 'piece': Piece.B, 'color': Color.white }, 
               'c3': { 'piece': Piece.Q, 'color': Color.white }
            }
      elif modal == "magnet":
         if puzzle == 1:
            return {
               'a1': { 'piece': Piece.K, 'color': Color.black }, 
               'b1': None,
               'c1': None, 
               'a2': None, 
               'b2': None, 
               'c2': { 'piece': Piece.R, 'color': Color.white }, 
               'a3': { 'piece': Piece.B, 'color': Color.white }, 
               'b3': { 'piece': Piece.B, 'color': Color.white }, 
               'c3': { 'piece': Piece.R, 'color': Color.white }
            }
         if puzzle == 2:
            return {
               'a1': None, 
               'b1': None,
               'c1': { 'piece': Piece.R, 'color': Color.white }, 
               'a2': { 'piece': Piece.K, 'color': Color.black }, 
               'b2': None, 
               'c2': None, 
               'a3': None, 
               'b3': { 'piece': Piece.N, 'color': Color.white }, 
               'c3': { 'piece': Piece.Q, 'color': Color.white }
            }
      elif modal == "begge":
         if puzzle == 1:
            return {
               'a1': { 'piece': Piece.K, 'color': Color.black }, 
               'b1': None,
               'c1': None, 
               'a2': { 'piece': Piece.P, 'color': Color.white },
               'b2': { 'piece': Piece.P, 'color': Color.white }, 
               'c2': None, 
               'a3': None,
               'b3': { 'piece': Piece.R, 'color': Color.white }, 
               'c3': { 'piece': Piece.Q, 'color': Color.white }
            }
         if puzzle == 2:
            return {
               'a1': { 'piece': Piece.K, 'color': Color.black },
               'b1': None,
               'c1': { 'piece': Piece.B, 'color': Color.white }, 
               'a2': { 'piece': Piece.P, 'color': Color.white }, 
               'b2': None,
               'c2': { 'piece': Piece.B, 'color': Color.white }, 
               'a3': { 'piece': Piece.R, 'color': Color.white }, 
               'b3': None, 
               'c3': None
            }
         