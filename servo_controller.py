
import RPi.GPIO as GPIO
import time
from square import *
from force import *
from controller import *

NORTH = 2.6
MID = 6.6
SOUTH = 10.6

class ServoController():

    def __init__(self, c):

        self.controller = c

        self.squares = {
            Square.A1: {
                "pins": { "photoResistor": 15, "led": 2, "servo": 26 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.A2: {
                "pins": { "photoResistor": 11, "led": 12, "servo": 19 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.A3: {
                "pins": { "photoResistor": 9, "led": 1, "servo": 13 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.B1: { # virker ikke
                "pins": { "photoResistor": 17, "led": 24, "servo": 16 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.B2: {
                "pins": { "photoResistor": 27, "led": 25, "servo": 21 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.B3: {
                "pins": { "photoResistor": 4, "led": 23, "servo": 6 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.C1: {
                "pins": { "photoResistor": 18, "led": 3, "servo": 0 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.C2: {
                "pins": { "photoResistor": 10, "led": 7, "servo": 5 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.C3: {
                "pins": { "photoResistor": 22, "led": 8, "servo": 20 },
                "state": { "occupied": False, "force": Force.neutral }
            }
        }

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for square in self.squares:
            GPIO.setup(self.squares[square]["pins"]["photoResistor"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.squares[square]["pins"]["led"], GPIO.OUT)
            GPIO.setup(self.squares[square]["pins"]["servo"], GPIO.OUT)
            GPIO.output(self.squares[square]["pins"]["led"], GPIO.LOW)
            self.squares[square]["servo"] = GPIO.PWM(self.squares[square]["pins"]["servo"], 50)
            self.squares[square]["servo"].start(6.6)


    def run(self):
        for square in self.squares:
            read = GPIO.input(self.squares[square]["pins"]["photoResistor"])
            isNowOccupied = False if read == 1 else True
            if isNowOccupied != self.squares[square]["state"]["occupied"]:
                self.squares[square]["state"]["occupied"] = isNowOccupied
                if isNowOccupied:
                    #print(square)
                    #self.squares[square]["servo"].ChangeDutyCycle(NORTH)
                    self.controller.board_placed_square(square)
                else:
                    #self.squares[square]["servo"].ChangeDutyCycle(SOUTH)
                    self.controller.board_lifted_square(square)
    
    def setLed(self, square, attackable):
        if attackable:
            GPIO.output(self.squares[square]["pins"]["led"], GPIO.HIGH)
        else:
            GPIO.output(self.squares[square]["pins"]["led"], GPIO.LOW)

    def setForce(self, square: Square, force: Force):
        currentForce = self.squares[square]["state"]["force"]
        if currentForce == force:
            return
        
        self.squares[square]["state"]["force"] = force

        if force == Force.neutral:
            self.squares[square]["servo"].ChangeDutyCycle(MID)
        elif force == Force.pull:
            self.squares[square]["servo"].ChangeDutyCycle(NORTH)
        elif force == Force.push:
            self.squares[square]["servo"].ChangeDutyCycle(SOUTH)


        
'''
class ServoController():

    def __init__(self, c):
        return

    def run(self):
        return
    
    def setForce(self, square, force):
        return

    def setLed(self, square, attackable):
        return
'''