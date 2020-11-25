#!/usr/bin/python

from square import *
from GUI import *
from controller import *
from board_controller import *
from servo_controller import *

import sys
import threading

class App(threading.Thread):

   def __init__(self):
      
      launch = sys.argv[1]
      
      self.controller = Controller()
      self.sc = ServoController(self.controller, launch)
      self.controller.servo = self.sc
      self.bc = BoardController(self.controller)
      self.controller.board = self.bc
      self.gui = GUI(self.bc, launch)
      threading.Thread.__init__(self)
      self.start()

      while True:
         self.sc.run()
         self.gui.start()

   def run(self):
      print("running")
       


if __name__ == "__main__":
   app = App()