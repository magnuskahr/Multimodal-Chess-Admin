import RPi.GPIO as GPIO
import time
from square import *
from force import *

NORTH = 2.6
MID = 6.6
SOUTH = 10.6

class ServoController():

    def __init__(self):

        self.squares = {
            Square.A1: {
                "pins": { "photoResistor": 22, "led": 8, "servo": 13 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.A2: {
                "pins": { "photoResistor": 10, "led": 7, "servo": 6 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.A3: {
                "pins": { "photoResistor": 18, "led": 3, "servo": 20 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.B1: { # virker ikke
                "pins": { "photoResistor": 27, "led": 25, "servo": 19 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.B2: {
                "pins": { "photoResistor": 15, "led": 2, "servo": 21 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.B3: {
                "pins": { "photoResistor": 9, "led": 1, "servo": 5 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.C1: {
                "pins": { "photoResistor": 17, "led": 24, "servo": 26 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.C2: {
                "pins": { "photoResistor": 4, "led": 23, "servo": 16 },
                "state": { "occupied": False, "force": Force.neutral }
            },
            Square.C3: {
                "pins": { "photoResistor": 11, "led": 12, "servo": 0 },
                "state": { "occupied": False, "force": Force.neutral }
            }
        }

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for square in self.squares:
            GPIO.setup(self.squares[square]["pins"]["photoResistor"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.squares[square]["pins"]["led"], GPIO.OUT)
            GPIO.setup(self.squares[square]["pins"]["servo"], GPIO.OUT)
            self.squares[square]["servo"] = GPIO.PWM(self.squares[square]["pins"]["servo"], 50)
            self.squares[square]["servo"].start(6.6)


    def run(self):
        return
        '''
        for square in self.squares:
            newReading = GPIO.input(self.squares[square]["pins"]["photoResistor"])
            if newReading != self.squares[square]["state"]["occupied"]:
                self.squares[square]["state"]["occupied"] = newReading
                if newReading is 1:
                    print(square)
                    self.squares[square]["servo"].ChangeDutyCycle(NORTH)
                else:
                    self.squares[square]["servo"].ChangeDutyCycle(SOUTH)
        '''
    
    def setForce(self, force: Force, square: Square):
        currentForce = self.squares["state"]["force"]
        if currentForce == force:
            return
        
        self.squares["state"]["force"] = force

        if force == Force.neutral:
            self.squares[square]["servo"].ChangeDutyCycle(MID)
        elif force == Force.pull:
            self.squares[square]["servo"].ChangeDutyCycle(NORTH)
        elif force == Force.push:
            self.squares[square]["servo"].ChangeDutyCycle(SOUTH)


        
'''
while True:
    for square in squares:
        newReading = GPIO.input(squares[square]["pins"]["photoResistor"])
        if newReading != squares[square]["state"]["occupied"]:
            squares[square]["state"]["occupied"] = newReading
            if newReading is 1:
                squares[square]["servo"].ChangeDutyCycle(NORTH)
            else:
                squares[square]["servo"].ChangeDutyCycle(SOUTH)
'''