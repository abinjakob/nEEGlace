# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 17:06:37 2024

@author: messung
"""

#!/usr/bin/env python
"""
Created on Wed May  3 16:59:39 2024

Real-time streaming of EEG from nEEGlace 
----------------------------------------
This script detects the EEG LSL live stream, continuously collects data, and streams
the EEG signal from all the channels. 

The script is orginally from the LabStreamingLayers Github example ReceiveAndPlot.py
https://github.com/labstreaminglayer/pylsl/blob/master/pylsl/examples/ReceiveAndPlot.py

Modified By: Abin Jacob
             Carl von Ossietzky University Oldenburg
             abin.jacob@uni-oldenburg.de
"""

# libraries
import numpy as np
import math
import pylsl
from pylsl import resolve_stream
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from pyqtgraph.Qt import QtCore
from typing import List
import sys

# parameters for the plotting window
# time period to show (in ms)
plotPeriod = 5  
# interval period between screen updates (in ms)
updateInterval = 60 
# interval period of pulling new data (in ms)
pullInterval = 500

# class to represent a plottable inlet
class Inlet:
    # constructor of Inlet
    def __init__(self, info: pylsl.StreamInfo):
        # creating inlet: 
        # max_buflen set to plot duration so that old data is discarded)
        # applied online click sync to make all streams in same time domain as local lsl_clock()
        self.inlet = pylsl.StreamInlet(info, max_buflen=plotPeriod, processing_flags=pylsl.proc_clocksync | pylsl.proc_dejitter)    
        # store the stream info
        self.name = info.name()
        self.nchan = info.channel_count()
    
    # function to pull data from inlet and plot it  
    def pullPlot(self, plotTime: float, plt: pg.PlotItem):
        # plot_time - lowest timestamp visible in plot
        # plt - plot the data should be shown on  
        pass


# class to handle multi-channel data
class DataInlet(Inlet):
    dtypes = [[], np.float32, np.float64, None, np.int32, np.int16, np.int8, np.int64]    
    # constructor of DataInlet
    def __init__(self, info: pylsl.StreamInfo, plt_main: pg.PlotItem, plt_ch7: pg.PlotItem):
        # calling the constructor of the super class
        super().__init__(info)
        # calculating size for buffer
        bufsize = (2 * math.ceil(info.nominal_srate() * plotPeriod), info.channel_count())
        # initialising the buffer
        self.buffer = np.empty(bufsize, dtype=self.dtypes[info.channel_format()])
        empty = np.array([])
        # creating curve object for each channel that will handle displaying the data
        self.curves = [pg.PlotCurveItem(x=empty, y=empty, autoDownsample=True) for _ in range(self.nchan)]
        for i, curve in enumerate(self.curves):
            # adding each curve to the appropriate subplot
            if i == 6:
                plt_ch7.addItem(curve)
            else:
                plt_main.addItem(curve)
        self.plt_ch7 = plt_ch7
    
    # function to pull new data chunks from a data stream, update the data buffer
    # and update the corresponding plots for each channel of data. 
    def pullPlot(self, plotTime, plt_main, plt_ch7):
        # pull new chunk of data from the data stream
        _, ts = self.inlet.pull_chunk(timeout=0.0, max_samples=self.buffer.shape[0], dest_obj=self.buffer)
        if ts:
            # converting timestamps to numpy
            ts = np.asarray(ts)
            vals = self.buffer[0:ts.size, :]
            new_ts = None
            oldOffset = 0
            newOffset = 0
            for ichan in range(self.nchan):
                # retrieve current plot data (old timestamps and values)
                old_ts, old_vals = self.curves[ichan].getData()
                if ichan == 0:
                    # calculating the portion of the old data that remains visible given the new plot time
                    oldOffset = old_ts.searchsorted(plotTime)
                    # same for the new data, in case we pulled more data than
                    # can be shown at once
                    newOffset = ts.searchsorted(plotTime)
                    # append new timestamps to the trimmed old timestamps
                    new_ts = np.hstack((old_ts[oldOffset:], ts[newOffset:]))
                # append new data to the trimmed old data
                new_vals = np.hstack((old_vals[oldOffset:], vals[newOffset:, ichan] - ichan))
                # replace the old data
                self.curves[ichan].setData(new_ts, new_vals)
                if ichan == 6:
                    self.plt_ch7.setYRange(-300,300)

def main():
    inlets: List[Inlet] = []
    print("Looking for nEEGlace...")
    # resolving streams
    # resolving streams
    streams = pylsl.resolve_stream('type', 'ExG')

    # setting up main plot window with two subplots
    win = pg.GraphicsLayoutWidget(show=True, title="nEEGlace EEG Stream")
    win.resize(1000, 600)

    plt_main = win.addPlot(row=0, col=0, title="EEG Stream")
    plt_ch7 = win.addPlot(row=1, col=0, title="Sound Onset")

    plt_main.enableAutoRange(x=False, y=True)
    plt_ch7.enableAutoRange(x=False, y=True)

    # iterate over found streams, creating specialized inlet objects that will
    # handle plotting the data
    for info in streams:
        if info.nominal_srate() != pylsl.IRREGULAR_RATE \
                and info.channel_format() != pylsl.cf_string:
            print('Connected to nEEGlace')
            inlets.append(DataInlet(info, plt_main, plt_ch7))
        else:
            print('nEEGlace not detected')

    # function to scroll the plot window along x-axis
    def scroll():
        fudgeFactor = pullInterval * .002
        plotTime = pylsl.local_clock()
        plt_main.setXRange(plotTime - plotPeriod + fudgeFactor, plotTime - fudgeFactor)
        plt_ch7.setXRange(plotTime - plotPeriod + fudgeFactor, plotTime - fudgeFactor)

    # function to update the data 
    def update():
        mintime = pylsl.local_clock() - plotPeriod
        # call pullPlot for each inlet.
        for inlet in inlets:
            inlet.pullPlot(mintime, plt_main, plt_ch7)

    # create a timer that will move the view every update interval
    updateTimer = QtCore.QTimer()
    updateTimer.timeout.connect(scroll)
    updateTimer.start(updateInterval)

    # create a timer that will pull and add new data occasionally
    pullTimer = QtCore.QTimer()
    pullTimer.timeout.connect(update)
    pullTimer.start(pullInterval)

    # Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()
        
if __name__ == '__main__':
    main()