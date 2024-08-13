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


# SET PARAMS ------------------------------------

# threshold for sound trigger
thresh = 5
# trigger channel in the stream
triggerChan = 7
# duration to look for sound trigger (in sec)
look4sound = 5

# common outputs of push2lsl
errstr1 = 'not recognized as an internal or external command'
errstr2 = 'DeviceNotFoundError'
successtr = 'Device info packet has been received. Connection has been established. Streaming...'
isConnected = False

# -----------------------------------------------

# libraries 
import os
import signal
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
from pylsl import StreamInlet, resolve_stream, StreamInfo

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
    time.sleep(3)
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

proc= None
try:    
    # if amp is on and advertising
    try:
        print('Connecting.... Please wait')
        # starting subprocess for push2lsl 
        # also capturing its standard output and error
        with subprocess.Popen('explorepy push2lsl -n Explore_84D1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True, universal_newlines=True) as proc:
            # continuously monitoring the output of subprocess
            for line in proc.stdout:  
                # checking if connection is made
                if successtr in line:
                    print(f'nEEGlace is connected. Pushing to LSL...{Style.RESET_ALL}')
                    isConnected = True
                    break
                # checking for error messages
                if errstr1 in line:
                    print(f'{Back.RED}ExplorePy is not installed{Style.RESET_ALL}')
                    print('Downlaod from: https://pypi.org/project/explorepy/')
                    proc.terminate()
                    sys.exit()
                if errstr2 in line:
                    print(f'{Back.RED}Unable to connect to nEEGlace{Style.RESET_ALL}')
                    print('Restart the Amplifier  and try again or long press the button until it blinks blue.')
                    proc.terminate()
                    sys.exit()                
                if not isConnected:
                    proc.terminate()
    except Exception as e:
        print(f'An error occurred: {e}')
    
    if isConnected:
        # resolve and initialise stream
        streams = resolve_stream('type', 'EEG')
        inlet = StreamInlet(streams[0])
        # retrieving sampling rate 
        srate = inlet.info().nominal_srate()
        time.sleep(2)
        print(f'\n{Back.GREEN}nEEGlace is Ready{Style.RESET_ALL} and streaming to LSL')
    else:
        print('Unable to connect to LSL stream. Try again..')
        sys.exit() 
    
    time.sleep(2)
    # checking the sound stream
    print(f'\n{Back.WHITE}Step 3:{Style.RESET_ALL}\nNow lets test the sound stream to check if it working fine')
    
    # function to process incoming data and detect triggers
    def detectSound():
        global soundDetector, sample
        sample = None
        # pull sample
        sample, timestamp = inlet.pull_sample(timeout= 1.0)
        # print(sample)
        if sample is None:
            return
        # check if trigger present
        if sample[triggerChan-1] > thresh:
            # print(sample)
            print(f'{Back.GREEN}Audio event detected{Style.RESET_ALL}')
            soundDetector = True
    
    # initialising counters 
    count = 0
    nosound = 0
    # running loop for sound check 3 times
    while count < 3 and nosound < 3:
        # print(sample)
        print('\nMake a loud sound')
        soundDetector = False
        start = time.time()
        # look for sound for short duration
        while time.time()-start < look4sound:
            detectSound()
            time.sleep(1/srate)
            # if sound detected increment counter
            if soundDetector:
                time.sleep(3)
                count += 1
                break
        # if sound not detected within the period
        if not soundDetector:
            nosound += 1
            if nosound < 3:
                print('Cannot detect sound.... Make a louder sound!')
            else:
                print('Unable to detect sound! Check if the Bella Board is powered and try again.')
                # sys.exit()
            
finally:
    if proc:
        proc.kill()

  


    
    
    
    
    
    
        
