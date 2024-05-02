#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 16:59:39 2024

Real-time streaming of EEG from nEEGlace 
----------------------------------------
This script detects the EEG LSL live stream, continuously collects data, and streams
the EEG signal from all the channels. 

@author: Abin Jacob
         Carl von Ossietzky University Oldenburg
         abin.jacob@uni-oldenburg.de
"""

# libraries 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pylsl import StreamInlet, resolve_stream


# printing status message
print("Looking for an EEG stream...")
# resolve and initialise EEG stream using LSL
streams = resolve_stream('type', 'EEG')  
inlet = StreamInlet(streams[0])
# retriving info from stream info
nchans = inlet.info().channel_count()
fs = inlet.info().nominal_srate()
# printing status message
print('EEG Stream Found...')
print('Stream Info:')
print(f'Channels: {nchans}, Sampling rate: {fs}')

# initialise figure window
fig, axes = plt.subplots(nchans, 1, figsize=(10, 6))
# time window to display in the plot (in ms)
timewindow = 10 
# converting to samples 
timesamples = int(timewindow * fs)
# to store EEG data for each channel
eegdata = np.zeros((timesamples, nchans))

# initialize plot lines
lines = []
for i, ax in enumerate(axes):
    line, = ax.plot(np.linspace(0, timewindow, timesamples), np.zeros(timesamples), lw= 1)
    lines.append(line)
    ax.set_xlim(0, timewindow)
    ax.set_ylim(-500, 500)  

# function to update plot
def updatePlot(frame):
    global eegdata
    # get new sample
    sample, timestamp = inlet.pull_sample()
    if sample:
        eegdata = np.roll(eegdata, -1, axis= 0)
        eegdata[-1, :] = sample
    for i, line in enumerate(lines):
        line.set_ydata(eegdata[:, i])
    return lines

# plotting 
ani = FuncAnimation(fig, updatePlot, blit= True, interval= 1)
plt.show()
