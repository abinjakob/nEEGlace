#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 19:32:51 2024

Online ERP Calculation for nEEGlace 
-----------------------------------
This script detects the EEG LSL live stream, continuously collects data,calculates 
the ERP for epochs created based on the sound triggers from channel 8 and plot the 
ERPs in real-time.

@author: Abin Jacob
         Carl von Ossietzky University Oldenburg
         abin.jacob@uni-oldenburg.de
"""

# libraries
import numpy as np
import matplotlib.pyplot as plt
import time

# using FuncAnimation for real-time visualisation
from matplotlib.animation import FuncAnimation
# for concurrent execution
import threading
# for LSL communication
from pylsl import StreamInlet, resolve_stream
# for high-pass filter
from scipy.signal import butter, filtfilt 


# SET PARAMS -----------------------------------------

# duration of the epoch 
epoch_duration = 0.8
# max epochs to compute ERP
maxTrials = 40
# threshold of the audio trigger signal at channel 8
trigger_threshold = 0.5
# trigger channel in the stream (must be always the last channel)
trigger_channel = 7

# high-pass filter to correct the dc offset
hp = 0.3
hp_order = 4
# ----------------------------------------------------


# printing status message
print("Looking for an EEG stream...")
# resolve and initialise EEG stream using LSL
streams = resolve_stream('type', 'EEG')  
inlet = StreamInlet(streams[0])
# retriving sampling rate from stream info
sampling_rate = inlet.info().nominal_srate()
print(f'Sampling rate: {sampling_rate}')

# channel index of the trigger
tidx = trigger_channel-1
# total number of channels 
nbchans = tidx 
# time points in single epoch 
epoch_samples = int(sampling_rate * epoch_duration)
# to temporarily store the eeg data for the current epoch
buffer = np.zeros((epoch_samples, nbchans)) 
# to store the sound triggers 
triggers = [] 
# to store all epochs  
epochs = []  


# function to design high-pass filter 
def butter_highpass(cutoff, fs, order= 5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype= 'high', analog= False)
    return b,a

# function to apply high-pass filter to signal
def highpass_filter(data, cutoff, fs, order= 5):
    b, a = butter_highpass(cutoff, fs, order= order)
    padlen = max(len(data) // 2 - 1, 0)
    filtered_data = filtfilt(b, a, data, padlen=padlen)
    return filtered_data

# function to process incoming data, detect triggers and storing epochs 
def process_data():
    global buffer, epochs, triggers
    sample, timestamp = inlet.pull_sample()
    # checking if trigger channel indicates an event
    if sample[tidx] > trigger_threshold:  
        print("Audio event detected. Collecting data...")
        # initialising to store triggers temporarily
        trigger_buffer = np.zeros(epoch_samples)
        for i in range(epoch_samples):
            sample, timestamp = inlet.pull_sample()
            # store EEG data for the current epoch 
            raw_eeg = sample[:nbchans]
            filtered_eeg = highpass_filter(raw_eeg, hp, sampling_rate, hp_order)
            buffer[i, :] = filtered_eeg 
            # store trigger for the current epoch
            trigger_buffer[i] = sample[tidx]
        # ensure epochs does not exceed maxTrials
        if len(epochs) >= maxTrials:
            epochs.pop(0)                               # deleting the old epochs     
        if len(triggers) >= maxTrials:
            triggers.pop(0)                             # deleting the old triggers    
        # append the new epoch to the epochs list
        epochs.append(buffer.copy())  
        # append the new trigger to the trigger list
        triggers.append(trigger_buffer.copy())
        
# function to calculate erp based on stored epochs
def update_average():
    # checking if the epochs contain data
    if epochs:
        # calculating ERP using the data stored in epochs 
        average_epoch = np.mean(np.array(epochs), axis=0)
        return average_epoch
    else:
        return None
    
# setting up Matplotlib for real-time plotting
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios': [3,1]})

# function to initialise plot
def init():
    # for erp plot
    ax1.set_xlim(0, epoch_samples)
    ax1.set_ylim(-100, 100)
    ax1.set_title('ERP')
    ax1.set_xlabel('time')
    ax1.set_ylabel('amplitude (mV)')
    # for trigger plot
    ax2.set_xlim(0, epoch_samples)
    ax2.set_ylim(-0.1, 10)
    ax2.set_title('Sound Triggers')
    ax2.set_xlabel('time')
    ax2.set_ylabel('amplitude (mV)')
    return ax1, ax2

# function to update plot
def update(frame):
    average_epoch = update_average()
    if average_epoch is not None:
        ax1.clear()
        ax2.clear()     
        # plotting ERP
        # loop over channels (except the trigger channel)
        for i in range(nbchans):  
            ax1.plot(average_epoch[:, i], label=f'Channel {i+1}', linewidth=0.5)
        # ax.legend()
        # plotting triggers 
        # checking if the trigger contain data
        if triggers:  
            latest_trigger = triggers[-1]
            ax2.plot(latest_trigger, label= 'Trigger', color='r', linewidth=0.5)
    return ax1, ax2

# create animation using FuncAnimation
# frame data caching is disabled for the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=100, cache_frame_data=False)
plt.show()


# Real-Time Data Processing
# using thread to concurrently run process_data() to check for new data and 
# to detect the triggers 

# function for real-time data processing 
def data_collection_loop():
    while True:
        # check for new data and process it
        process_data()
        # to ensure data is processed in alignment with the sampling rate
        time.sleep(1/sampling_rate)  

# starting data collection in a separate thread
thread = threading.Thread(target=data_collection_loop)
# daemonise thread
thread.daemon = True  
thread.start()

# showing plot with real-time updating
plt.show()

# showing plot with real-time updating
plt.show()
