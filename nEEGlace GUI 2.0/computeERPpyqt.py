# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:11:58 2024

@author: messung
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
from scipy.signal import butter, filtfilt
import threading
import pylsl
import time 

# Initialize ERP parameters
def initialize_erp_params(inlet, srate, nchan, plot_widget, epoch_duration=0.8, maxtrials=40, trigger_thr=0.03,
                          trigger_chan=7, high_pass=0.3, hp_ord=4, channels_to_select=None, channels_to_diff=None):
    global epochs, triggers, buffer, sampling_rate, epoch_samples, trigger_channel, trigger_threshold, hp, hp_order
    global chan2sel, chan2diff, tidx, max_trials, trial_count, erp_plot_widget
    
    # Initialize parameters
    epochs = []
    triggers = []
    buffer = np.zeros((int(srate * epoch_duration), nchan-1))
    trial_count = 0

    sampling_rate = srate
    epoch_samples = int(srate * epoch_duration)
    trigger_channel = trigger_chan
    trigger_threshold = trigger_thr
    hp = high_pass
    hp_order = hp_ord
    max_trials = maxtrials
    tidx = trigger_chan - 1
    chan2sel = [x - 1 for x in (channels_to_select or [])]
    chan2diff = [x - 1 for x in (channels_to_diff or [])]
    erp_plot_widget = plot_widget


# High-pass filter
def butter_highpass(cutoff, fs, order=2):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def highpass_filter(data, cutoff, fs, order=2):
    b, a = butter_highpass(cutoff, fs, order)
    return filtfilt(b, a, data)

# Detect trigger and process data
def process_data(inlet):
    global epochs, triggers, buffer, trial_count, raw_eeg

    timestamp, sample = inlet.pullsample()
    if sample is not None and sample[tidx] > trigger_threshold:
        trial_count += 1
        for i in range(epoch_samples):
            timestamp, sample = inlet.pullsample()
            if sample is not None:
                raw_eeg = [sample[j] for j in range(len(sample)) if j != tidx]
                # filtered_eeg = highpass_filter(raw_eeg, hp, sampling_rate, hp_order)
                # buffer[i, :] = filtered_eeg
                buffer[i, :] = raw_eeg

        # Store the epoch
        if len(epochs) >= max_trials:
            epochs.pop(0)
        epochs.append(buffer.copy())


# Update ERP plot
def update_erp_plot():
    global erp_plot_widget, epochs
    if not epochs:
        return

    # Calculate average ERP
    average_epoch = np.mean(np.array(epochs), axis=0)
    # print(f"average_epoch shape: {average_epoch.shape}")
    erp_plot_widget.clear()

    # Plot selected channels
    if chan2sel:
        erp_plot_widget.plot(average_epoch[:, chan2sel[0]], pen=pg.mkPen('b', width=2))
    else:
        for i in range(average_epoch.shape[1]):
            erp_plot_widget.plot(average_epoch[:, i], pen=pg.mkPen('w', width=1))

# Start a separate thread for data collection
def data_loop(inlet):
    while True:
        process_data(inlet)  
        QtCore.QCoreApplication.processEvents() 
        time.sleep(0.01)

# Start ERP processing and plotting
def plotERP(inlet, srate, nchan, plot_widget):
    initialize_erp_params(inlet, srate, nchan, plot_widget)

    

    data_thread = threading.Thread(target=data_loop, args=(inlet,), daemon=True)
    data_thread.start()
    
    # Use a timer for plot updates
    timer = QtCore.QTimer()
    timer.timeout.connect(update_erp_plot)
    timer.setInterval(100)  
    timer.start()
    return timer
    

    
