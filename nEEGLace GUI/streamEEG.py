# plot_stream.py
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5.QtWidgets import QApplication
import pylsl
import numpy as np
import sys
class DataInletPlotter:
    def __init__(self, inlets, plt_main, plt_ch7, plotPeriod: int = 5, pullInterval: int = 500):
        self.inlets = inlets
        self.plt_main = plt_main
        self.plt_ch7 = plt_ch7
        self.plotPeriod = plotPeriod
        self.pullInterval = pullInterval
        self.curves = []  # Store PlotDataItems for each channel

        # Initialize PlotDataItem for each channel and add to the plot
        for inlet in self.inlets:
            for i in range(inlet.nchan):
                curve = pg.PlotDataItem()  # Create PlotDataItem
                if i == 6:
                    self.plt_ch7.addItem(curve)  # Add to channel 7 plot
                else:
                    self.plt_main.addItem(curve)  # Add to main plot
                self.curves.append(curve)

    def pullPlot(self, inlet, plotTime):
        ts, vals = inlet.pull_data()
        
        if len(ts):  # Check if there are valid timestamps
            new_ts = None
            oldOffset, newOffset = 0, 0
            
            for ichan in range(inlet.nchan):
                curve = self.curves[ichan]  # Get the PlotDataItem for this channel
    
                # Retrieve current plot data (old timestamps and values)
                old_ts, old_vals = curve.getData()
                
                if old_ts is None or len(old_ts) == 0:
                    # If old_ts is None or empty, initialize it as an empty array
                    old_ts = np.array([])
                    old_vals = np.array([])
    
                if ichan == 0:
                    # Only calculate the offsets for the first channel
                    oldOffset = np.searchsorted(old_ts, plotTime)
                    newOffset = np.searchsorted(ts, plotTime)
                    # Append new timestamps to the trimmed old timestamps
                    new_ts = np.hstack((old_ts[oldOffset:], ts[newOffset:]))
                
                # Append new data to the trimmed old data
                new_vals = np.hstack((old_vals[oldOffset:], vals[newOffset:, ichan] - ichan))
                
                # Update the curve with new data
                curve.setData(new_ts, new_vals)


    def update(self):
        mintime = pylsl.local_clock() - self.plotPeriod
        for inlet in self.inlets:
            self.pullPlot(inlet, mintime)

    def scroll(self):
        fudgeFactor = self.pullInterval * .002
        plotTime = pylsl.local_clock()
        self.plt_main.setXRange(plotTime - self.plotPeriod + fudgeFactor, plotTime - fudgeFactor)
        self.plt_ch7.setXRange(plotTime - self.plotPeriod + fudgeFactor, plotTime - fudgeFactor)

def setup_plot_window():
    # Create plot window
    win = pg.GraphicsLayoutWidget(show=True, title="nEEGlace EEG Stream")
    win.resize(1000, 600)
    
    plt_main = win.addPlot(row=0, col=0, title="EEG Stream")
    plt_ch7 = win.addPlot(row=1, col=0, title="Channel 7")
    
    plt_main.enableAutoRange(x=False, y=True)
    plt_ch7.enableAutoRange(x=False, y=True)
    
    return win, plt_main, plt_ch7

def plotEEG(inlets, plotPeriod: int = 5, updateInterval: int = 60, pullInterval: int = 500):
    app = QApplication([])
    win, plt_main, plt_ch7 = setup_plot_window()

    plotter = DataInletPlotter(inlets, plt_main, plt_ch7, plotPeriod, pullInterval)

    # Set up scrolling
    updateTimer = QtCore.QTimer()
    updateTimer.timeout.connect(plotter.scroll)
    updateTimer.start(updateInterval)

    # Set up data pulling
    pullTimer = QtCore.QTimer()
    pullTimer.timeout.connect(plotter.update)
    pullTimer.start(pullInterval)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()
