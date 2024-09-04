# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:52:14 2024

nEEGlace GUI
------------
The script is an attempt to create basic user interface for nEEGlace in
python using Tkinter

@author: Abin Jacob
         Carl von Ossietzky University Oldenburg
         abin.jacob@uni-oldenburg.de
"""

# params ---------------------------------------------------

# root path
rootpath = r'C:\Users\messung\Desktop\nEEGlace GUI'
# config file
configfilename = 'nEEGlaceConfigfile.txt' 

# threshold for sound detection
soundThresh = 5
# trigger channel in the stream 
triggerChan = 7
# period to look for sound trigger (in sec)
look4sound = 5

# common outputs of push2lsl
errstr1   = 'not recognised as an internal or external command'
errstr2   = 'DeviceNotFoundError'
successtr = 'Device info packet has been received. Connection has been established. Streaming...'

# ----------------------------------------------------------



# libraries
import time
import os
import signal
# interface
import tkinter 
import customtkinter
# subprocess
import subprocess
import threading 
# for ssh connection with Bela
import paramiko
# lsl
from pylsl import StreamInlet, StreamInfo, resolve_stream

# set directory
os.chdir(r'C:\Users\messung\Desktop\nEEGlace GUI') 
from belaconnect import checkBelaStatus, getBelaConfig, dumpBelaConfig

# open the config file and fetch data
configfile = os.path.join(rootpath, configfilename)
# function to read text file
def readConfig():
    with open(configfile, 'r') as f:
        lines = f.readlines()
    return lines
# function to fetch data from config file
def fetchConfig():   
    global bela_micgain, bela_thresh, bela_record, bela_recorddur, stream_erpavg, stream_tmin, stream_tmax
    # read lines from config file
    configlines = readConfig()
    # fetching data
    bela_micgain   = int(configlines[0])
    bela_thresh    = float(configlines[1])
    bela_record    = int(configlines[2])
    bela_recorddur = int(configlines[3])
    stream_erpavg  = int(configlines[4])
    stream_tmin    = float(configlines[5])
    stream_tmax    = float(configlines[6])   
    return bela_micgain, bela_thresh, bela_record, bela_recorddur, stream_erpavg, stream_tmin, stream_tmax

# function to dump data to config file
def dumpConfig():
    with open(configfile, 'w') as f:
        f.writelines(f'{bela_micgain}\n')
        f.writelines(f'{bela_thresh}\n')
        f.writelines(f'{bela_record}\n')
        f.writelines(f'{bela_recorddur}\n')
        f.writelines(f'{stream_erpavg}\n')
        f.writelines(f'{stream_tmin}\n')
        f.writelines(f'{stream_tmax}\n')

# function to read and update from the Bela config file
def updateConfig():
    global belastatus
    configlines = readConfig()
    belavalues, belastatus = getBelaConfig()
    if belastatus:    
        configlines[0] = f'{belavalues[1]}\n'
        configlines[1] = f'{belavalues[0]}\n'
        configlines[2] = f'{belavalues[2]}\n'
        configlines[3] = f'{belavalues[3]}\n'
        with open(configfile, 'w') as f:
            f.writelines(configlines)
        

# function to dump config settings to Bela board 
def updateBela():
    configlines = readConfig()
    values = [configlines[0], configlines[1], configlines[2], configlines[3]]
    time.sleep(1)
    writestatus = dumpBelaConfig(values)
    return writestatus
        



# system settings 
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

# app frame
app = customtkinter.CTk()
app.geometry('720x480')
app.title('nEEGlace GUI')
proc = None

# function to handle closing the window
def on_closingwindow():
    global proc, killstatus
    if proc is not None:
        proc.terminate()
        proc.wait()
        killstatus = 1
        try:
            proc.wait(timeout=5)
            killstatus = 2
        except subprocess.TimeoutExpired:
            proc.kill()
            killstatus = 3
        
        try:
            if proc.poll() is None:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                killstatus = 4
        except Exception as e:
            print(f'Error killing explorepy: {e}')
            killstatus = 5
    app.quit()
    app.destroy()

# setting the protocol to handle window close
app.protocol("WM_DELETE_WINDOW", on_closingwindow)

# font styles 
H1 = ('Arial', 24, 'bold')
H2 = ('Arial', 20, 'bold')
H3 = ('Arial', 16, 'bold')
B1 = ('Arial', 14)
B2 = ('Arial', 12)
B3 = ('Arial', 10)

# color palette 
UItextbox = {'active': {'boxbg': '#343638', 'boxborder': '#565b5e', 'boxfont': '#ffffff'},
                  'deactive': {'boxbg': '#2b2b2b', 'boxborder': '#343638', 'boxfont': '#5f5f5f'}}
UIfont = {'normal': '#ffffff', 'notes': '#5f5f5f','deactive': '#5f5f5f', 'error': '#f34444', 'success': '#2cd756'}

# configure grid layout 
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)


    


# --- app frames ---

# main frame 
mainFrame= customtkinter.CTkFrame(app)
mainFrame.grid(row=0, column=0, sticky='nsew')

# troubleshoot frame 1
troubleshootFrame1= customtkinter.CTkFrame(app)
troubleshootFrame1.grid(row=0, column=0, sticky='nsew')
troubleshootFrame1.grid_forget()

# troubleshoot frame 2
troubleshootFrame2= customtkinter.CTkFrame(app)
troubleshootFrame2.grid(row=0, column=0, sticky='nsew')
troubleshootFrame2.grid_forget()

# troubleshoot frame 3
troubleshootFrame3= customtkinter.CTkFrame(app)
troubleshootFrame3.grid(row=0, column=0, sticky='nsew')
troubleshootFrame3.grid_forget()

# configure frame
configFrameMain = customtkinter.CTkFrame(app)
configFrameMain.grid(row=0, column=0, sticky='nsew')
configFrameMain.grid_forget()

# streamerFrame
streamerFrameMain = customtkinter.CTkFrame(app)
streamerFrameMain.grid(row=0, column=0, sticky='nsew')
streamerFrameMain.grid_forget()

# configure grid layout for frames (add all frames here)
for frame in (mainFrame, troubleshootFrame1, troubleshootFrame2, troubleshootFrame3, configFrameMain, streamerFrameMain):
    frame.grid_rowconfigure(9, weight=1)
    for i in range(10):
        frame.grid_columnconfigure(i, weight=1)




# --- main frame UI ---

# button functions
def on_troubleshoot():
    mainFrame.grid_forget()
    troubleshootFrame1.grid(sticky='nsew')
def on_config():
    mainFrame.grid_forget()
    configFrameMain.grid(sticky='nsew')
    updateConfig()
def on_start():
    mainFrame.grid_forget()
    streamerFrameMain.grid(sticky='nsew')

# title 
title = customtkinter.CTkLabel(mainFrame, text= 'Welcome to nEEGlace', font=H1)
title.grid(row=0, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (40,0))
# body text '
bodystr = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor\nincididunt ut labore et dolore magna aliqua.'
body = customtkinter.CTkLabel(mainFrame, text= bodystr, font=B2, text_color='#979797', justify= 'left')
body.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (10,0))

# troubleshoot button
BTtroubleshoot = customtkinter.CTkButton(mainFrame, text= 'Troubleshoot', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f',
                                         command= on_troubleshoot)
BTtroubleshoot.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))
# setup buttons
BTconfig = customtkinter.CTkButton(mainFrame, text= 'Configure nEEGlace', fg_color='#ffffff', text_color='#000000', hover_color='#979797',
                                   command= on_config)
BTconfig.grid(row=9, column=1, sticky='sw', padx= (0,10), pady= (0,40))
# start recording button
BTstart = customtkinter.CTkButton(mainFrame, text= 'Start Streaming', 
                                  command= on_start)
BTstart.grid(row=9, column=9, sticky='se', padx= (10,40), pady= (0,40))




# --- troubleshoot frame1 UI ---
# checking if the device is on

# button functions
def on_t1back():
    troubleshootFrame1.grid_forget()
    mainFrame.grid(sticky='nsew')
    
def on_t1next():
    if t1_Q1radioInput.get()==0:
        t1_Q1label.configure(text= 'Cant turn on nEEGlace! Please try again after charging the battery', text_color='#f34444')
    else:
        t1_Q1label.configure(text= '', text_color='#2cd756')
        troubleshootFrame1.grid_forget()
        troubleshootFrame2.grid(sticky='nsew')
        
    
# title 
t1_title =  customtkinter.CTkLabel(troubleshootFrame1, text= 'Setup nEEGlace', font=H2)
t1_title.grid(row=0, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (40,0))
# device status
t1_devicestat = customtkinter.CTkLabel(troubleshootFrame1, text= 'Device Status:', font=B2, text_color='#979797', justify= 'left')
t1_devicestat.grid(row=1, column=0, sticky='w', padx= (40,0), pady= (2,0))
t1_devicestatans = customtkinter.CTkLabel(troubleshootFrame1, text= '-', font=B2, text_color='#979797', justify= 'left')
t1_devicestatans.grid(row=1, column=0, sticky='w', padx= (125,0), pady= (2,0))
t1_ampstat = customtkinter.CTkLabel(troubleshootFrame1, text= 'Amplifier Status:', font=B2, text_color='#979797', justify= 'left')
t1_ampstat.grid(row=1, column=1, sticky='w', padx= (0,0), pady= (2,0))
t1_ampstatans = customtkinter.CTkLabel(troubleshootFrame1, text= '-', font=B2, text_color='#979797', justify= 'left')
t1_ampstatans.grid(row=1, column=1, sticky='w', padx= (100,0), pady= (2,0))
# body font
t1_body1 = customtkinter.CTkLabel(troubleshootFrame1, text= 'Step 1', font=H3, justify= 'left')
t1_body1.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (0,0))
t1_bodystr = 'Turn on nEEglace by flipping the switch situated on the right\nside of the device'
t1_body2 = customtkinter.CTkLabel(troubleshootFrame1, text= t1_bodystr, font=B1, justify= 'left')
t1_body2.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (60,0))

# ask if the device is on
t1_Q1str = 'Can you see a red light next to the switch?'
t1_Q1 = customtkinter.CTkLabel(troubleshootFrame1, text= t1_Q1str, font=B1, text_color='#979797', justify= 'left')
t1_Q1.grid(row=3, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (0,0))
# radio button int variable for input
t1_Q1radioInput = tkinter.IntVar(value=0)
t1_Q1radio1 = customtkinter.CTkRadioButton(troubleshootFrame1, text= 'Yes', variable=t1_Q1radioInput, value= 1)
t1_Q1radio1.grid(row=3, column=0, sticky='w', padx=(40, 0), pady=(60, 0))
t1_Q1radio2 = customtkinter.CTkRadioButton(troubleshootFrame1, text= 'No', variable=t1_Q1radioInput, value= 0)
t1_Q1radio2.grid(row=4, column=0, sticky='w', padx=(40, 0), pady=(8, 0))

# error label
t1_Q1label = customtkinter.CTkLabel(troubleshootFrame1, text= '', font=B2, justify= 'left')
t1_Q1label.grid(row=9, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (0,10))

# back button
t1_BTback2main = customtkinter.CTkButton(troubleshootFrame1, text= 'Back to Main Menu', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f', 
                                 command= on_t1back)
t1_BTback2main.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))
# next button
t1_BTnext = customtkinter.CTkButton(troubleshootFrame1, text= 'Next  >>', 
                                 command= on_t1next)
t1_BTnext.grid(row=9, column=9, sticky='se', padx= (10,40), pady= (0,40))




# --- troubleshoot frame2 UI ---
# checking the status of the Mentalab amp

# function to connect to stream
def t2connectStream():
    global isConnected, streamStatus, proc
    # initialising glob variables 
    isConnected  = False
    streamStatus = 0
    try:
        # start a subprocess for push2lsl
        # also captures its standard output and error
        with subprocess.Popen('explorepy push2lsl -n Explore_84D1', shell= True, stdout= subprocess.PIPE, stderr= subprocess.STDOUT, bufsize= 1, text= True, universal_newlines= True) as proc:
            # continuous monitoring output of subprocess#
            for line in proc.stdout:
                # check if connection is made
                if successtr in line:
                    streamStatus = 1
                    isConnected = True
                    break
                # check for errors 
                if errstr1 in line:
                    streamStatus = 2
                    break
                if errstr2 in line:
                    streamStatus = 3
                    break
        if not isConnected:
            proc.terminate()
    except Exception as e:
        streamStatus = 4

# button functions
def on_t2back():
    troubleshootFrame2.grid_forget()
    mainFrame.grid(sticky='nsew')
def on_t2prev():
    troubleshootFrame2.grid_forget()
    troubleshootFrame1.grid(sticky='nsew')
def on_t2next():
    if t2_Q1radioInput.get()==1:
        t2_Q1label.configure(text= 'nEEGlace is in Offline mode! Cant stream data.', text_color='#f34444')
    elif t2_Q1radioInput.get()==2:
        t2_Q1label.configure(text= 'Amplifier is starting up. Wait for sometime until it turns blue.', text_color='#f34444')
    elif t2_Q1radioInput.get()==3:
        t2_Q1label.configure(text= 'Amplifier has low battery! Need to charge the Amplifier.', text_color='#f34444')       
    else:
        t2_ampstatans.configure(text= 'Bluetooth ON', text_color='#569cff')
        t2_Q1label.configure(text= 'Connecting to LSL network', text_color='#ffffff')
        # disable button
        t2_BTback2main.configure(state='disabled')
        t2_BTprev.configure(state='disabled')
        t2_BTnext.configure(state='disabled')
        # disable options
        t2_Q1radio1.configure(state='disabled')
        t2_Q1radio2.configure(state='disabled')
        t2_Q1radio3.configure(state='disabled')
        t2_Q1radio4.configure(state='disabled')
        
        # run progressbar
        t2_bar.grid(row=9, column=1, sticky='w', padx= (20,0), pady= (0,60))
        t2_bar.start()
        
        # attempt connection (starting in different thread to avoid UI being frozen)
        connectionThread = threading.Thread(target= t2connectStream)
        connectionThread.start()
        # continuously checking streamStatus
        checkThread(connectionThread)

# function to continuously check streamStatus from the thread
stopCheck = False
def checkThread(connectionThread):
    global streams, inlet, srate, nbchans, stopCheck
    # checks every 100ms if thread is complete
    if connectionThread.is_alive():
        if not stopCheck:    
            troubleshootFrame2.after(300, lambda: checkThread(connectionThread))
        if streamStatus == 1:
            try:
                stream  = resolve_stream('type', 'EEG')
                inlet   = StreamInlet(stream[0])
                srate   = inlet.info().nominal_srate()
                nbchans = inlet.info().channel_count()
                print('LSL stream connected')
                t2_bar.stop()
                t2_bar.grid_forget()
                t2_Q1label.configure(text= 'Connected')
                troubleshootFrame2.grid_forget()
                troubleshootFrame3.grid(sticky='nsew')
                stopCheck = True
            except Exception as e:
                print('Unable to connect to LSL stream')                     
    # if complete
    else:
        # check connection status
        if streamStatus == 2:
            t2_bar.stop()
            t2_bar.grid_forget()
            t2_Q1label.configure(text= 'Error: ExplorePy is not installed', text_color='#f34444')
        elif streamStatus == 3:
            t2_bar.stop()
            t2_bar.grid_forget()
            t2_Q1label.configure(text= 'Error: Restart and try again. Also kill the explorepy subprocess from Windows Task Manager if exist', text_color='#f34444')    
        elif streamStatus == 4:
            t2_bar.stop()
            t2_Q1label.configure(text= 'Error: Unable to connect to nEEGlace. Restart and try again.', text_color='#f34444')
        
            

# title 
t2_title =  customtkinter.CTkLabel(troubleshootFrame2, text= 'Troubleshoot nEEGlace', font=H2)
t2_title.grid(row=0, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (40,0))
# device status
t2_devicestat = customtkinter.CTkLabel(troubleshootFrame2, text= 'Device Status:', font=B2, text_color='#979797', justify= 'left')
t2_devicestat.grid(row=1, column=0, sticky='w', padx= (40,0), pady= (2,0))
t2_devicestatans = customtkinter.CTkLabel(troubleshootFrame2, text= 'ON', font=B2, text_color='#2cd756', justify= 'left')
t2_devicestatans.grid(row=1, column=0, sticky='w', padx= (125,0), pady= (2,0))
t2_ampstat = customtkinter.CTkLabel(troubleshootFrame2, text= 'Amplifier Status:', font=B2, text_color='#979797', justify= 'left')
t2_ampstat.grid(row=1, column=1, sticky='w', padx= (0,0), pady= (2,0))
t2_ampstatans = customtkinter.CTkLabel(troubleshootFrame2, text= '-', font=B2, text_color='#979797', justify= 'left')
t2_ampstatans.grid(row=1, column=1, sticky='w', padx= (100,0), pady= (2,0))
# body font
t2_body1 = customtkinter.CTkLabel(troubleshootFrame2, text= 'Step 2', font=H3, justify= 'left')
t2_body1.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (0,0))
t2_bodystr = 'Please turn on the Amplifier by pressing the button on the top\nleft of the nEEGlace'
t2_body2 = customtkinter.CTkLabel(troubleshootFrame2, text= t2_bodystr, font=B1, justify= 'left')
t2_body2.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (60,0))

# ask if the device is on
t2_Q1str = 'What light do you see on the amp?'
t2_Q1 = customtkinter.CTkLabel(troubleshootFrame2, text= t2_Q1str, font=B1, text_color='#979797', justify= 'left')
t2_Q1.grid(row=3, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (0,0))
# radio button int variable for input
t2_Q1radioInput = tkinter.IntVar(value=0)
t2_Q1radio1 = customtkinter.CTkRadioButton(troubleshootFrame2, text= 'Blinking Blue', variable=t2_Q1radioInput, value= 0)
t2_Q1radio1.grid(row=3, column=0, sticky='w', padx=(40, 0), pady=(60, 0))
t2_Q1radio2 = customtkinter.CTkRadioButton(troubleshootFrame2, text= 'Blinking Green', variable=t2_Q1radioInput, value= 1)
t2_Q1radio2.grid(row=4, column=0, sticky='w', padx=(40, 0), pady=(8, 0))
t2_Q1radio3 = customtkinter.CTkRadioButton(troubleshootFrame2, text= 'Blinking Pink', variable=t2_Q1radioInput, value= 2)
t2_Q1radio3.grid(row=5, column=0, sticky='w', padx=(40, 0), pady=(8, 0))
t2_Q1radio4 = customtkinter.CTkRadioButton(troubleshootFrame2, text= 'Blinking Red & Turned off', variable=t2_Q1radioInput, value= 3)
t2_Q1radio4.grid(row=6, column=0, columnspan= 2, sticky='w', padx=(40, 0), pady=(8, 0))

# error label
t2_Q1label = customtkinter.CTkLabel(troubleshootFrame2, text= '', font=B2, justify= 'left')
t2_Q1label.grid(row=9, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (0,60))
t2_bar = customtkinter.CTkProgressBar(troubleshootFrame2, progress_color= '#ffffff', height= 2, corner_radius=2)

# back button
t2_BTback2main = customtkinter.CTkButton(troubleshootFrame2, text= 'Back to Main Menu', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f', 
                                 command= on_t2back)
t2_BTback2main.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))
# previous button 
t2_BTprev = customtkinter.CTkButton(troubleshootFrame2, text= '<<  Prev', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f', 
                                 command= on_t2prev)
t2_BTprev.grid(row=9, column=9, sticky='se', padx= (0,190), pady= (0,40))
# next button
t2_BTnext = customtkinter.CTkButton(troubleshootFrame2, text= 'Next  >>',
                                    command= on_t2next)
t2_BTnext.grid(row=9, column=9, sticky='se', padx= (10,40), pady= (0,40))




# --- troubleshoot frame3 UI ---
def detectSound():
    global soundDetector, sample
    sample = None
    # pull sample
    sample, timestamp = inlet.pull_sample(timeout= 1.0)
    if sample is None:
        return
    # check if trigger present 
    if sample[triggerChan-1] > soundThresh:
        print('sound detected')
        soundDetector = True

# button functions
def on_t3start():
    # start a new top level window
    testAudioWindow = customtkinter.CTkToplevel(troubleshootFrame3)
    testAudioWindow.title('Test Audio')
    testAudioWindow.geometry('400x200')
    # restricting window resize
    testAudioWindow.resizable(False, False)
    
    def on_tawclose():
        testAudioWindow.destroy()
        testAudioWindow.update()
    
    count = 0
    nosound = 0
    
    # while count<3 and nosound<3:  
    # body text
    taw_makesound = customtkinter.CTkLabel(testAudioWindow, text= 'Make a Loud', font=B1)
    taw_makesound.pack(pady=(10,0))
    taw_feedback = customtkinter.CTkLabel(testAudioWindow, text= '', font=H1, text_color='#2cd756')
    taw_feedback.pack(pady=(10,0))
            
            
        
        
        
    # close button 
    taw_BTclose = customtkinter.CTkButton(testAudioWindow, text= 'Close', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f',
                                          command= on_tawclose)
    taw_BTclose.pack(pady= (100,0))
    

# title 
t3_title =  customtkinter.CTkLabel(troubleshootFrame3, text= 'Troubleshoot nEEGlace', font=H2)
t3_title.grid(row=0, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (40,0))
# device status
t3_devicestat = customtkinter.CTkLabel(troubleshootFrame3, text= 'Device Status:', font=B2, text_color='#979797', justify= 'left')
t3_devicestat.grid(row=1, column=0, sticky='w', padx= (40,0), pady= (2,0))
t3_devicestatans = customtkinter.CTkLabel(troubleshootFrame3, text= 'ON', font=B2, text_color='#2cd756', justify= 'left')
t3_devicestatans.grid(row=1, column=0, sticky='w', padx= (125,0), pady= (2,0))
t3_ampstat = customtkinter.CTkLabel(troubleshootFrame3, text= 'Amplifier Status:', font=B2, text_color='#979797', justify= 'left')
t3_ampstat.grid(row=1, column=1, sticky='w', padx= (0,0), pady= (2,0))
t3_ampstatans = customtkinter.CTkLabel(troubleshootFrame3, text= 'Streaming', font=B2, text_color='#2cd756', justify= 'left')
t3_ampstatans.grid(row=1, column=1, sticky='w', padx= (100,0), pady= (2,0))
# body font
t3_body1 = customtkinter.CTkLabel(troubleshootFrame3, text= 'Step 2', font=H3, justify= 'left')
t3_body1.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (0,0))
t3_bodystr = 'Now lets test the sound stream to check\nif nEEGlace is able to detect the audio'
t3_body2 = customtkinter.CTkLabel(troubleshootFrame3, text= t2_bodystr, font=B1, justify= 'left')
t3_body2.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (60,0))
# instructions
t3_Q1str = 'Click on the Start Testing Audio button below and make loud \nsounds to test the audio detection'
t3_Q1 = customtkinter.CTkLabel(troubleshootFrame3, text= t3_Q1str, font=B1, text_color='#979797', justify= 'left')
t3_Q1.grid(row=3, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (40,0))

# quit button
t3_BTquit = customtkinter.CTkButton(troubleshootFrame3, text= 'Quit Stream', fg_color='#5b2b2b', text_color='#b6b6b6', hover_color='#4f2121')
t3_BTquit.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))
# start button
t3_BTstartsoundcheck = customtkinter.CTkButton(troubleshootFrame3, text= 'Start Testing Audio',
                                               command= on_t3start)
t3_BTstartsoundcheck.grid(row=9, column=9, sticky='se', padx= (10,40), pady= (0,40))




# --- Configure Main Frame UI ---

# button functions
def on_cfgmback():
    configFrameMain.grid_forget()
    mainFrame.grid(sticky='nsew')
    
def on_cfgmsave():
    global bela_micgain, bela_thresh, bela_record, bela_recorddur, stream_erpavg, stream_tmin, stream_tmax, belawritestatus
    bela_micgain   = cfgM_gainentry.get() 
    bela_thresh    = cfgM_threshentry.get()
    bela_record    = cfgM_recordtoggleVar.get()
    bela_recorddur = cfgM_durentry.get()
    stream_erpavg  = cfgM_trlavgentry.get()
    stream_tmin    = cfgM_epminentry.get()
    stream_tmax    = cfgM_epmaxentry.get()
    
    # check input conditions
    if int(bela_micgain) > 55:
       bela_micgain = '55' 
       cfgM_gainentry.delete(0, 'end')
       cfgM_gainentry.insert(0, bela_micgain)
       tkinter.messagebox.showwarning("Warning", "Microphone gain exceeds the maximum allowed value of 55. It has been reset to 55.")
    
    if int(bela_recorddur) > 720:
       bela_recorddur = '720' 
       cfgM_durentry.delete(0, 'end')
       cfgM_durentry.insert(0, bela_recorddur)
       tkinter.messagebox.showwarning("Warning", "Recorde duration exceeds the maximum allowed value of 720sec. It has been reset to 720sec.")
    
    
    
    
    # write data to config file
    dumpConfig()
    # update bela
    belastatus = checkBelaStatus()
    if belastatus:    
        belawritestatus = updateBela()
        if not belawritestatus:
            cfgM_infonotestr = 'Error saving to Bela Board. Verify the connection and try again'
            cfgM_infonote.configure(text = cfgM_infonotestr, text_color= UIfont['error'])
            
        else:
            cfgM_infonotestr = 'Changes made to the settings are saved'
            cfgM_infonote.configure(text = cfgM_infonotestr, text_color= UIfont['success'])
            
            # Switch frames after 2 seconds without freezing the GUI
            configFrameMain.after(1400, lambda: (configFrameMain.grid_forget(), mainFrame.grid(sticky='nsew')))
    else:
        cfgM_infonotestr = 'Changes made to the settings are saved'
        cfgM_infonote.configure(text = cfgM_infonotestr, text_color= UIfont['success'])
        
        # Switch frames after 2 seconds without freezing the GUI
        configFrameMain.after(1400, lambda: (configFrameMain.grid_forget(), mainFrame.grid(sticky='nsew')))
    
    
    
def cfgM_recordtoggleEvent():
    if cfgM_recordtoggleVar.get() == 1:
        cfgM_durentry.configure(state= 'normal', border_color= '#565b5e', fg_color= '#343638', text_color= UItextbox['active']['boxfont'])
        cfgM_recordtoggle.configure(text= 'ON')
    if cfgM_recordtoggleVar.get() == 0:
        cfgM_durentry.configure(state= 'disabled', border_color= '#343638', fg_color= '#2b2b2b', text_color= UItextbox['deactive']['boxfont'])
        cfgM_recordtoggle.configure(text= 'OFF')
        
        
# fetch config data
updateConfig()
configdata = fetchConfig()

# title 
cfgM_title =  customtkinter.CTkLabel(configFrameMain, text= 'Configure nEEGlace', font=H2)
cfgM_title.grid(row=0, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (40,0))
# bela setings
cfgM_title1 = customtkinter.CTkLabel(configFrameMain, text= 'Bela Board Settings', font=B1, text_color='#979797', justify= 'left')
cfgM_title1.grid(row=1, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (40,0))
# input gain
cfgM_gaintxt = customtkinter.CTkLabel(configFrameMain, text= 'Microphone Input Gain', font=B1)
cfgM_gaintxt.grid(row=2, column=0, sticky='w', padx= (40,0), pady= (10,0))
cfgM_gainentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_gainentry.insert(0, configdata[0])
cfgM_gainentry.grid(row=2, column=2, sticky='w', padx= (10,0), pady= (10,0))
# energy threshold
cfgM_threshtxt = customtkinter.CTkLabel(configFrameMain, text= 'Energy Threshold', font=B1)
cfgM_threshtxt.grid(row=3, column=0, sticky='w', padx= (40,0), pady= (0,0))
cfgM_threshentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_threshentry.insert(0, configdata[1])
cfgM_threshentry.grid(row=3, column=2, sticky='w', padx= (10,0), pady= (10,0))
# audio setings
cfgM_title2 = customtkinter.CTkLabel(configFrameMain, text= 'Audio Recording', font=B1, text_color='#979797', justify= 'left')
cfgM_title2.grid(row=4, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (20,0))
# record audio
cfgM_recordtxt = customtkinter.CTkLabel(configFrameMain, text= 'Record Audio', font=B1)
cfgM_recordtxt.grid(row=5, column=0, sticky='w', padx= (40,0), pady= (10,0))
cfgM_recordtoggleVar = customtkinter.IntVar()
cfgM_recordtoggleVar.set(configdata[2])
# setting values based on record status 
if cfgM_recordtoggleVar.get() == 1:
    toggletext = 'ON'
    dur_state = 'normal'
    dur_border = UItextbox['active']['boxborder']
    dur_fg = UItextbox['active']['boxbg']
    dur_txtclr = UItextbox['active']['boxfont']
elif cfgM_recordtoggleVar.get() == 0:
    toggletext = 'OFF'
    dur_state = 'disabled'
    dur_border = UItextbox['deactive']['boxborder']
    dur_fg = UItextbox['deactive']['boxbg']
    dur_txtclr = UItextbox['deactive']['boxfont']
cfgM_recordtoggle = customtkinter.CTkSwitch(configFrameMain, variable= cfgM_recordtoggleVar, text= toggletext,
                                            onvalue= 1, offvalue= 0, command= cfgM_recordtoggleEvent)
cfgM_recordtoggle.grid(row=5, column=2, sticky='w', padx= (10,0), pady= (10,0))
# # record duration
cfgM_durtxt = customtkinter.CTkLabel(configFrameMain, text= 'Record Duration (s)', font=B1)
cfgM_durtxt.grid(row= 6, column=0, sticky='w', padx= (40,0), pady= (10,0))
cfgM_durentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_durentry.insert(0, configdata[3])
cfgM_durentry.configure(state= dur_state, border_color= dur_border, fg_color= dur_fg, text_color= dur_txtclr)

cfgM_durentry.grid(row=6, column=2, sticky='w', padx= (10,0), pady= (10,0))
# stream settings 
cfgM_title3 = customtkinter.CTkLabel(configFrameMain, text= 'Stream Settings', font=B1, text_color='#979797', justify= 'left')
cfgM_title3.grid(row=1, column=7, columnspan= 5, sticky='w', padx= (0,0), pady= (40,0))
# trial averaged gain
cfgM_trlavgtxt = customtkinter.CTkLabel(configFrameMain, text= 'Trial to Average for ERP', font=B1)
cfgM_trlavgtxt.grid(row=2, column=7, sticky='w', padx= (0,0), pady= (10,0))
cfgM_trlavgentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_trlavgentry.insert(0, configdata[4])
cfgM_trlavgentry.grid(row=2, column=9, sticky='w', padx= (10,0), pady= (10,0))
# epoch min
cfgM_epmintxt = customtkinter.CTkLabel(configFrameMain, text= 'Epoch Min (s)', font=B1)
cfgM_epmintxt.grid(row=3, column=7, sticky='w', padx= (0,0), pady= (10,0))
cfgM_epminentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_epminentry.insert(0, configdata[5])
cfgM_epminentry.grid(row=3, column=9, sticky='w', padx= (10,0), pady= (10,0))
# epoch max
cfgM_epmaxtxt = customtkinter.CTkLabel(configFrameMain, text= 'Epoch Max (s)', font=B1)
cfgM_epmaxtxt.grid(row=4, column=7, sticky='w', padx= (0,0), pady= (0,0))
cfgM_epmaxentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_epmaxentry.insert(0, configdata[6])
cfgM_epmaxentry.grid(row=4, column=9, sticky='w', padx= (10,0), pady= (0,0))

# info note
cfgM_infonotestr = ''
cfgM_infonote = customtkinter.CTkLabel(configFrameMain, text= cfgM_infonotestr, font=B2, text_color= UIfont['notes'], justify= 'left')
cfgM_infonote.grid(row=8, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (24,0))

# back button
cfgM_BTback2main = customtkinter.CTkButton(configFrameMain, text= 'Back to Main Menu', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f', 
                                 command= on_cfgmback)
cfgM_BTback2main.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))

# save button
cfgM_BTsave = customtkinter.CTkButton(configFrameMain, text= 'Save Changes',
                                    command= on_cfgmsave)
cfgM_BTsave.grid(row=9, column=9, sticky='se', padx= (10,40), pady= (0,40))

if not belastatus:
    cfgM_gaintxt.configure(text_color= UIfont['deactive'])
    cfgM_gainentry.configure(state= 'disabled', border_color= UItextbox['active']['boxborder'], fg_color= UItextbox['deactive']['boxbg'], text_color= UItextbox['deactive']['boxfont'])
    cfgM_threshtxt.configure(text_color= UIfont['deactive'])
    cfgM_threshentry.configure(state= 'disabled', border_color= UItextbox['active']['boxborder'], fg_color= UItextbox['deactive']['boxbg'], text_color= UItextbox['deactive']['boxfont'])
    cfgM_recordtxt.configure(text_color= UIfont['deactive'])
    cfgM_recordtoggle.configure(state= 'disabled', fg_color= UItextbox['deactive']['boxborder'])
    cfgM_durtxt.configure(text_color= UIfont['deactive'])
    cfgM_durentry.configure(state= 'disabled', border_color= UItextbox['active']['boxborder'], fg_color= UItextbox['deactive']['boxbg'], text_color= UItextbox['deactive']['boxfont'])
    # info note
    cfgM_infonotestr = 'NOTE: Bela board is not connected to the computer. To make changes to the Bela Board Settings, Connect Bela Board \nto computer via USB and click Connect Bela.'
    cfgM_infonote.configure(text = cfgM_infonotestr)
    # connect bella button
    cfgM_BTconnectbela = customtkinter.CTkButton(configFrameMain, text= 'Connect Bela', fg_color='#ffffff', text_color='#000000', hover_color='#979797',
                                       command= on_config)
    cfgM_BTconnectbela.grid(row=9, column=2, sticky='sw', padx= (0,10), pady= (0,40))




# --- Streamer Main Frame UI ---

# title 
strM_title =  customtkinter.CTkLabel(streamerFrameMain, text= 'Stream nEEGlace', font=H2)
strM_title.grid(row=0, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (40,0))
# body text '
strM_bodystr = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor\nincididunt ut labore et dolore magna aliqua.'
strM_body = customtkinter.CTkLabel(streamerFrameMain, text= bodystr, font=B2, text_color='#979797', justify= 'left')
strM_body.grid(row=2, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (10,0))


# stream info
strM_title1 = customtkinter.CTkLabel(streamerFrameMain, text= 'Sream Info', font=B1, text_color='#979797', justify= 'left')
strM_title1.grid(row=3, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (60,0))
# sfreq
sfreq = 40
strM_sfreqtxt = customtkinter.CTkLabel(streamerFrameMain, text= 'Sampling Frequency', font=B1)
strM_sfreqtxt.grid(row=4, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (10,0))
strM_sfreqans = customtkinter.CTkLabel(streamerFrameMain, text= f'{sfreq} Hz', font=B1)
strM_sfreqans.grid(row=4, column=2, columnspan= 5, sticky='w', padx= (0,0), pady= (10,0))
# channel count
nchan = 8
strM_nchantxt = customtkinter.CTkLabel(streamerFrameMain, text= 'Number of Channels', font=B1)
strM_nchantxt.grid(row=5, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (0,0))
strM_nchanans = customtkinter.CTkLabel(streamerFrameMain, text= f'{nchan} Channels', font=B1)
strM_nchanans.grid(row=5, column=2, columnspan= 5, sticky='w', padx= (0,0), pady= (0,0))
# trigger count
trgchan = 7
strM_trgchantxt = customtkinter.CTkLabel(streamerFrameMain, text= 'Trigger Channel', font=B1)
strM_trgchantxt.grid(row=6, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (0,0))
strM_trgchanans = customtkinter.CTkLabel(streamerFrameMain, text= f'{trgchan}', font=B1)
strM_trgchanans.grid(row=6, column=2, columnspan= 5, sticky='w', padx= (0,0), pady= (0,0))
# audio recording status
recordstaus = 'On'
strM_recordtxt = customtkinter.CTkLabel(streamerFrameMain, text= 'Audio Recording', font=B1)
strM_recordtxt.grid(row=7, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (0,0))
strM_recordans = customtkinter.CTkLabel(streamerFrameMain, text= f'{recordstaus}', font=B1)
strM_recordans.grid(row=7, column=2, columnspan= 5, sticky='w', padx= (0,0), pady= (0,0))

# plot info
strM_title3 = customtkinter.CTkLabel(streamerFrameMain, text= 'Plot Info', font=B1, text_color='#979797', justify= 'left')
strM_title3.grid(row=3, column=7, columnspan= 5, sticky='w', padx= (0,0), pady= (60,0))
# trials averaged
trlcount = 15
strM_trlavgtxt = customtkinter.CTkLabel(streamerFrameMain, text= 'Trial Count', font=B1)
strM_trlavgtxt.grid(row=4, column=7, columnspan= 5, sticky='w', padx= (0,0), pady= (10,0))
strM_trlavgans = customtkinter.CTkLabel(streamerFrameMain, text= f'{trlcount}', font=B1)
strM_trlavgans.grid(row=4, column=9, sticky='w', padx= (80,0), pady= (10,0))
# sound detector
sndstat = 'Sound Detected'
strM_sndstattxt = customtkinter.CTkLabel(streamerFrameMain, text= 'Trigger', font=B1)
strM_sndstattxt.grid(row=5, column=7, columnspan= 5, sticky='w', padx= (0,0), pady= (0,0))
strM_sndstatans = customtkinter.CTkLabel(streamerFrameMain, text= f'{sndstat}', font=B1, text_color='#2cd756')
strM_sndstatans.grid(row=5, column=9, columnspan= 5, sticky='w', padx= (80,0), pady= (0,0))

# quit button
strM_BTquit = customtkinter.CTkButton(streamerFrameMain, text= 'Quit Stream', fg_color='#5b2b2b', text_color='#b6b6b6', hover_color='#4f2121')
strM_BTquit.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))
# ERP button 
strM_BTerp = customtkinter.CTkButton(streamerFrameMain, text= 'Show ERP', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f')
strM_BTerp.grid(row=9, column=9, sticky='se', padx= (0,190), pady= (0,40))
# Plot Stream button
strM_BTeegstream = customtkinter.CTkButton(streamerFrameMain, text= 'Plot EEG Data', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f')
strM_BTeegstream.grid(row=9, column=9, sticky='se', padx= (10,40), pady= (0,40))


# run app
app.mainloop()
