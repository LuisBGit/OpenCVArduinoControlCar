# ! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.


import serial
import math
import pygame
import _thread

stringOut = "0,0"
LeftMotor = 0
RightMotor = 0


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        global LeftMotor, RightMotor, stringOut
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                LeftMotor = math.floor(self.controller.get_axis(1) * -150);
                RightMotor = math.floor(self.controller.get_axis(3) * -150);





def sendStream(left, right):
    stringOut = str(left) + "," + str(right)
    ser.write(bytes(stringOut, "ascii"))

if __name__ == "__main__":

    ser = serial.Serial('COM4', 38400, timeout=0)
    _thread.start_new_thread(sendStream, (LeftMotor,RightMotor))

    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()