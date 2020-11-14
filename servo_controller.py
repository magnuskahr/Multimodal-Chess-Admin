import RPi.GPIO as GPIO
import time

squares = {
    1: {
        "pins": { "photoResistor": 11, "led": 12, "servo": 0 },
        "state": { "occupied": False }
    },
    2: {
        "pins": { "photoResistor": 9, "led": 1, "servo": 5 },
        "state": { "occupied": False }
    },
    3: {
        "pins": { "photoResistor": 10, "led": 7, "servo": 6 },
        "state": { "occupied": False }
    },
    4: {
        "pins": { "photoResistor": 22, "led": 8, "servo": 13 },
        "state": { "occupied": False }
    },
    5: {
        "pins": { "photoResistor": 27, "led": 25, "servo": 19 },
        "state": { "occupied": False }
    },
    6: {
        "pins": { "photoResistor": 17, "led": 24, "servo": 26 },
        "state": { "occupied": False }
    },
    7: {
        "pins": { "photoResistor": 4, "led": 23, "servo": 16 },
        "state": { "occupied": False }
    },
    8: {
        "pins": { "photoResistor": 15, "led": 2, "servo": 21 },
        "state": { "occupied": False }
    }
}

GPIO.setmode(GPIO.BCM)

for square in squares:
    GPIO.setup(squares[square]["pins"]["photoResistor"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(squares[square]["pins"]["led"], GPIO.OUT)
    GPIO.setup(squares[square]["pins"]["servo"], GPIO.OUT)
    squares[square]["servo"] = GPIO.PWM(squares[square]["pins"]["servo"], 50)
    squares[square]["servo"].start(6.6)

while True:
    continue