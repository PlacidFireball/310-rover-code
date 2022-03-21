### EGEN 310R Runner Script

### Resources: 
# Servo control article: https://www.learnrobotics.org/blog/raspberry-pi-servo-motor/

import RPi.GPIO as GPIO
from time import sleep

def servoSetAngle(angle):
    pass

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) # Initialize pin 11 for output

servo = GPIO.PWM(11, 50) # Send a 50 Hz signal to the servo on pin 11
servo.start(0)

# Constants will have to change as we figure out duty for our servos
servo.ChangeDutyCycle(5) # left 90 degrees
sleep(1)
servo.ChangeDutyCycle(7.5) # neutral
sleep(1)
servo.ChangeDutyCycle(10) # right 90 degrees
sleep(1)

servo.stop() # stop the servo
GPIO.cleanup() # general cleanup