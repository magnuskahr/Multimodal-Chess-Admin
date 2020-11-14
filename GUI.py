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

   def __init__(self, board_controller):

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

      randomButton = Button(controls, text = "Random", command = self.random, bg = "white", fg = "black")
      randomButton.pack()

   def clear(self):
      self.board_controller.clearAll()
      self.board_controller.clearForces()

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
   
   def random(self):
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

      randomBoard = random.choice(self.boards)
      for square in randomBoard:
         if randomBoard[square] != None:
            piece = randomBoard[square]['piece']
            color = randomBoard[square]['color']
            self.board_controller.place(piece, color, e(square))
         else:
            self.board_controller.clear(e(square))


   def start(self):
      #self.window.mainloop()
      tk.update_idletasks()
      tk.update()
