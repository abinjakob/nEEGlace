# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 16:43:30 2024

@author: messung
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



# -- params 

# duration of the epoch 
epoch_duration = 0.8
# max epochs to compute ERP
maxTrials = 40
# threshold of the audio trigger signal at channel 8
trigger_threshold = 0.5
# trigger channel in the stream (must be always the last chasnnel)
trigger_channel = 7

# high-pass filter to correct the dc offset
hp = 0.3
hp_order = 4


# TO CALCULATE AVERAGE ERP OF SELECTED CHANNELS 
# channel to calculate average ERP                          -- (leave 'chan2sel' empty to calculate ERP for all channels separately)
chan2sel = []    
# subtract avg ERP of certain channels from chan2sel        -- (leave 'chan2diff' empty to calculate average ERP of 'chan2sel')
chan2diff = []  

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
def process_data(inlet, tidx, thresh, epoch_duration, maxTrials):
    global buffer, epochs, triggers
    sample, timestamp = inlet.pull_sample()
    # checking if trigger channel indicates an event
    if sample[tidx] > thresh:  
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