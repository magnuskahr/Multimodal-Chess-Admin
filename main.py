from square import *
from GUI import *
from board_controller import *
import threading

class App(threading.Thread):

   def __init__(self):
      self.bc = BoardController()
      self.gui = GUI(self.bc)
      threading.Thread.__init__(self)
      self.start()
      self.gui.start()

   def run(self):
      print("running")
       


if __name__ == "__main__":
   app = App()