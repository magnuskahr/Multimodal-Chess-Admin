from square import *
from GUI import *
from board_controller import *
from servo_controller import *
import threading

class App(threading.Thread):

   def __init__(self):
      self.sc = ServoController()
      self.bc = BoardController(self.sc)
      self.gui = GUI(self.bc)
      threading.Thread.__init__(self)
      self.start()

      while True:
         self.sc.run()
         self.gui.start()

   def run(self):
      print("running")
       


if __name__ == "__main__":
   app = App()