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
print('EEG Stream Found...')
# retriving info from stream info
nchans = inlet.info().channel_count()
fs = inlet.info().nominal_srate()
print('Stream Info:')
print(f'Channels: {nchans}, Sampling rate: {fs}')

maxsamples = int(10 * fs)


fig, axes = plt.subplots(nchans, 1, figsize=(10, 2*nchans))
lines = []
data = []

# Initialize lines and data structures
for ax in axes:
    line, = ax.plot([], [], lw=2)
    lines.append(line)
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)  # Modify the limits based on expected EEG signal ranges
    data.append([])

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(frame):
    sample, timestamp = inlet.pull_sample()
    for i in range(nchans):
        data[i].append(sample[i])
        if len(data[i]) > 100:  # Keep only the last 100 samples
            data[i].pop(0)
    timestamps = [timestamp - (len(data[0]) - i) * fs for i in range(len(data[0]))]  # Assuming 100 Hz sampling
    for j, line in enumerate(lines):
        line.set_data(timestamps, data[j])
        axes[j].set_xlim(timestamps[0], timestamps[-1])
    return lines

ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50)
plt.tight_layout()
plt.show()



