# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:58:31 2024

nEEGLace setup
--------------
This script is used to make the setting up of nEEGlace smoother. The script guides
the user through the start up procedures, detect any issue and also to test the 
audio streams are working as expected. 

@author: Abin Jacob
         Carl von Ossietzky University Oldenburg
         abin.jacob@uni-oldenburg.de
"""

# libraries 
import numpy as np
import math
import pylsl
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from pyqtgraph.Qt import QtCore
from typing import List
import sys
import subprocess
import time
# for coloured terminal text
from colorama import init as colorama_init
from colorama import Fore, Back, Style
import logging


# creating a welcome message 
print('\n-------------------------')
print('Welcome to nEEGlace setup')
print('-------------------------')
time.sleep(2)
# turn on the battery
print(f'\n{Back.WHITE}Step 1:{Style.RESET_ALL}\nPlease turn on nEEGlace by fliping the switch on the right side')
# check if it is on
count = 0
while count<3:
    time.sleep(1)
    userinput = input('\nCan you see a red light next to the switch? [Y/N]:')
    if userinput.lower() == 'n':
        time.sleep(1)
        print(f'{Back.RED}Low Battery! Please try again after charging the battery.{Style.RESET_ALL}')
        sys.exit()
    elif userinput.lower() == 'y':
        time.sleep(1)
        print(f'{Back.GREEN}nEEGlace is ON{Style.RESET_ALL}')
        break
    else:
        print('Wrong input. Press Y for yes and N for no')
        count +=1
else:
    print('Program ended...')
    sys.exit()
    

time.sleep(2)
# turn on the amp
print(f'\n{Back.WHITE}Step 2:{Style.RESET_ALL}\nPlease turn on the Amplifier by pressing the button on the top left of the nEEGlace')
# check if is on
count = 0
ampstate = 0 
while count < 5:
    time.sleep(1)
    print('\nWhat blinking light do you see on the amp?')
    print(f'1. {Back.BLUE}Blue{Style.RESET_ALL}, 2. {Back.GREEN}Green{Style.RESET_ALL}, 3. {Back.MAGENTA}Pink{Style.RESET_ALL}, 4. Blinked {Back.RED}Red{Style.RESET_ALL} and turned off{Style.RESET_ALL}')
    userinput = input('Enter color? [1/2/3/4]:')
    if userinput == '1':
        # amp is advertising
        time.sleep(1)
        print(f'{Back.BLUE}nEEGlace bluetooth is ON{Style.RESET_ALL}')
        ampstate = 1
        break
    elif userinput == '2':
        time.sleep(1)
        # amp is in offline mode 
        print('nEEGlace is in offline mode. Press the button twice to make it online')
        count +=1
    elif userinput == '3':
        time.sleep(1)
        # amp is booting up
        print('Wait for sometime until it turns blue')
        count +=1
    elif userinput == '4':
        time.sleep(1)
        # amp is booting up
        print(f'{Back.RED}Low Battery! Need to charge the Amplifier.{Style.RESET_ALL}')
        sys.exit()
    else:
        print('Wrong input. Press 1, 2 or 3')
        count +=1     
else:
    print('Program ended...')
    sys.exit()

# common errors with push2lsl
errstr1 = 'not recognized as an internal or external command'
errstr2 = 'DeviceNotFoundError'

# if amp is on and advertising
if ampstate == 1:
    try:
        print('Connecting.... Please wait')
        # starting subprocess for push2lsl  
        # also capturing its standard output and error
        process = subprocess.Popen('explorepy push2lsl -n Explore_84D1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # waiting for the process to finish
        process.wait()
        
        # reading the error output
        errorOut = process.stderr.read().decode('utf-8')
        
        if errorOut:
            print(errorOut)
            if errstr1 in errorOut:
                print(f'{Back.RED}ExplorePy is not installed{Style.RESET_ALL}')
                print('Downlaod from: https://pypi.org/project/explorepy/')
                sys.exit()
                
            elif errstr2 in errorOut:
                print(f'{Back.RED}Unable to connect to nEEGlace{Style.RESET_ALL}')
                print('Restart the device and try again.')
                sys.exit()
        else:
            print('Pushing to LSL...')
    except Exception as e:
        # If any other exception occurs, print it
        print(f'Error: {e}')
        sys.exit()
