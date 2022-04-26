### EGEN 310R Runner Script
### Written by Jared Weiss at Montana State University
### Resources:
# Servo control article: https://www.learnrobotics.org/blog/raspberry-pi-servo-motor/
# YouTube Livestream article: https://www.makeuseof.com/tag/live-stream-youtube-raspberry-pi/
# pigpio docs: https://docs.juliahub.com/PiGPIO/8aGxa/0.2.0/api/
# minimize servo jitter: https://ben.akrin.com/raspberry-pi-servo-jitter/

###JOYSTICK CONTROL INFO:
###Left Joystick: Axis 0, 1
###    - 1 Up (-1) down (1)
###    - 0 Left (-1) right (1)
###Right Joystick: Axis 2, 3
###    - 3 Up (-1) down (1)
###    - 2 Left (-1) right (1)
###Left Trigger: Axis 5
###    - (-1 no press) (1 full press)
###Right Trigger: Axis 4
###A button -> button 0
###B button -> button 1
###X -> 3
###Y -> 4
###D-Pad:(Hat)Up Down Left Right
###      (0, 1) (0, -1) (-1, 0) (1, 0)

import pygame
import RPi.GPIO as GPIO
from time import sleep
import pigpio
import os
import subprocess
import platform

def servoSetAngle(servo, angle):
    scaled = 500 + angle/180 * 2000 # want to write values between 500 and 2500
    pwm.set_servo_pulsewidth(servo, scaled)

os.environ["SDL_VIDEODRIVER"] = "dummy"

# Dictionary of our servo names to pins on the Pi - may be subject to change
servos = {"drivetrain" : 21, "servo" : 17,
          "arm_up_down" : 18, "arm_rotate" : 22,
          "articulation" : 27, "bucket" : 23}

# pigpio initialization
pwm = pigpio.pi() # start up the daemon
for name, pin in servos.items(): 
    print(f"Initializing: {name} on pin {pin}")
    pwm.set_mode(pin, pigpio.OUTPUT) # set each pin to output
    pwm.set_PWM_frequency(pin, 50)   # with 50 hz signal

# tentative guess for initializing the drivetrain
servoSetAngle(servos["drivetrain"], 90)
sleep(2)

pygame.display.init() # initialize a dummy display
pygame.init()         # initialize the pygame module for controller input
clock = pygame.time.Clock() # make a clock so we can get accurate timing should we need it

done = False
# Initialize the joysticks.
pygame.joystick.init()

# -------- Main Program Loop -----------
while not done:
    # Get rid of events that pygame generates because we
    # do not care about them at all
    pygame.event.clear()
    # Get count of joysticks and stick all the joystick objects
    # into a cute little list 
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    # For each joystick:
    for joystick in joysticks:
        print(joystick.get_name()) # log debug info to the console
        axes = joystick.get_numaxes()
        for i in range(axes): # do different stuff with each one
            axis = joystick.get_axis(i)
            if (i == 0): 
                servoSetAngle(servos["servo"]       , (axis+1)*90) # servo gos through full range of motion
            if (i == 1):
                servoSetAngle(servos["drivetrain"]  , (axis+1)*90) # drivetrain probably needs to be toned down
            if (i == 2):
                servoSetAngle(servos["arm_rotate"]  , (axis+1)*15) # arm rotation may need to be toned up as we stabilize it
            if (i == 3):
                servoSetAngle(servos["arm_up_down"] , (axis+1)*90) # arm up and down full range
            if (i == 4):
                servoSetAngle(servos["articulation"], (axis+1)*60) # articulation (second servo on arm) with diminished range
            if (i == 5):
                servoSetAngle(servos["bucket"]      , -1*(axis+1)*45+90) # bucket servo
            print("Axis {} value: {:>6.3f}".format(i, axis))

        buttons = joystick.get_numbuttons()
        print("Number of buttons: {}".format(buttons))

        # Exit on the B button
        for i in range(buttons):
            button = joystick.get_button(i)
            if (i == 1):
                if (button):
                    done = True
            print("Button {:>2} value: {}".format(i, button))
    
    clock.tick(20)

pygame.quit()
for name, pin in servos.items():
    print(f"Cleaning up {name} on pin {pin}")
    pwm.set_PWM_dutycycle(pin, 0)
    pwm.set_PWM_frequency(servo, 0)
    
# End egen310.py