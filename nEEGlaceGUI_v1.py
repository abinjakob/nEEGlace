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

# libraries
import tkinter 
import customtkinter
import time


# system settings 
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

# app frame
app = customtkinter.CTk()
app.geometry('720x480')
app.title('nEEGlace GUI')

# function to handle closing the window
def on_closingwindow():
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

# configure frame
configFrameMain = customtkinter.CTkFrame(app)
configFrameMain.grid(row=0, column=0, sticky='nsew')
configFrameMain.grid_forget()

# streamerFrame
streamerFrameMain = customtkinter.CTkFrame(app)
streamerFrameMain.grid(row=0, column=0, sticky='nsew')
streamerFrameMain.grid_forget()

# configure grid layout for frames (add all frames here)
for frame in (mainFrame, troubleshootFrame1, troubleshootFrame2, configFrameMain, streamerFrameMain):
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
        # run progressbar
        t2_bar.grid(row=9, column=1, sticky='w', padx= (20,0), pady= (0,60))
        t2_bar.start()
        # troubleshootFrame1.grid_forget()
        # troubleshootFrame2.grid(sticky='nsew')
        

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




# --- Configure Main Frame UI ---

# button functions
def on_cfgmsave():
    configFrameMain.grid_forget()
    mainFrame.grid(sticky='nsew')
def cfgM_recordtoggleEvent():
    if cfgM_recordtoggleVar.get() == 1:
        cfgM_durentry.configure(state= 'normal', border_color= '#565b5e', fg_color= '#343638')
        cfgM_recordtoggle.configure(text= 'ON')
    if cfgM_recordtoggleVar.get() == 0:
        cfgM_durentry.configure(state= 'disabled', border_color= '#343638', fg_color= '#2b2b2b')
        cfgM_recordtoggle.configure(text= 'OFF')
        
def on_cfgsave():
    print(f'Gain      : {cfgM_gainentry.get()}')
    print(f'Threshold : {cfgM_threshentry.get()}')
    if cfgM_recordtoggleVar.get() == 1:
        print(f'Record Duration : {cfgM_durentry.get()}')
        

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
cfgM_gainentry.grid(row=2, column=2, sticky='w', padx= (10,0), pady= (10,0))
# energy threshold
cfgM_threshtxt = customtkinter.CTkLabel(configFrameMain, text= 'Energy Threshold', font=B1)
cfgM_threshtxt.grid(row=3, column=0, sticky='w', padx= (40,0), pady= (0,0))
cfgM_threshentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_threshentry.grid(row=3, column=2, sticky='w', padx= (10,0), pady= (10,0))
# audio setings
cfgM_title2 = customtkinter.CTkLabel(configFrameMain, text= 'Audio Recording', font=B1, text_color='#979797', justify= 'left')
cfgM_title2.grid(row=4, column=0, columnspan= 5, sticky='w', padx= (40,0), pady= (20,0))
# record audio
cfgM_recordtxt = customtkinter.CTkLabel(configFrameMain, text= 'Record Audio', font=B1)
cfgM_recordtxt.grid(row=5, column=0, sticky='w', padx= (40,0), pady= (10,0))
cfgM_recordtoggleVar = customtkinter.IntVar()
cfgM_recordtoggle = customtkinter.CTkSwitch(configFrameMain, variable= cfgM_recordtoggleVar, text= 'OFF',
                                            onvalue= 1, offvalue= 0, command= cfgM_recordtoggleEvent)
cfgM_recordtoggle.grid(row=5, column=2, sticky='w', padx= (10,0), pady= (10,0))
# # record duration
cfgM_durtxt = customtkinter.CTkLabel(configFrameMain, text= 'Audio Record Duration', font=B1)
cfgM_durtxt.grid(row= 6, column=0, sticky='w', padx= (40,0), pady= (10,0))
cfgM_durentry = customtkinter.CTkEntry(configFrameMain, width= 48, state= 'disabled', border_color= '#343638', fg_color= '#2b2b2b')
cfgM_durentry.grid(row=6, column=2, sticky='w', padx= (10,0), pady= (10,0))
# stream settings 
cfgM_title3 = customtkinter.CTkLabel(configFrameMain, text= 'Stream Settings', font=B1, text_color='#979797', justify= 'left')
cfgM_title3.grid(row=1, column=7, columnspan= 5, sticky='w', padx= (0,0), pady= (40,0))
# trial averaged gain
cfgM_trlavgtxt = customtkinter.CTkLabel(configFrameMain, text= 'Trial to Average for ERP', font=B1)
cfgM_trlavgtxt.grid(row=2, column=7, sticky='w', padx= (0,0), pady= (10,0))
cfgM_trlavgentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_trlavgentry.grid(row=2, column=9, sticky='w', padx= (10,0), pady= (10,0))
# epoch min
cfgM_epmintxt = customtkinter.CTkLabel(configFrameMain, text= 'Epoch Min (s)', font=B1)
cfgM_epmintxt.grid(row=3, column=7, sticky='w', padx= (0,0), pady= (10,0))
cfgM_epminentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_epminentry.grid(row=3, column=9, sticky='w', padx= (10,0), pady= (10,0))
# epoch max
cfgM_epmaxtxt = customtkinter.CTkLabel(configFrameMain, text= 'Epoch Max (s)', font=B1)
cfgM_epmaxtxt.grid(row=4, column=7, sticky='w', padx= (0,0), pady= (0,0))
cfgM_epmaxentry = customtkinter.CTkEntry(configFrameMain, width= 48)
cfgM_epmaxentry.grid(row=4, column=9, sticky='w', padx= (10,0), pady= (0,0))
# info note
cfgM_infonotestr = 'Note: Please make sure Bela board is connected to the computer to reflect the changes you make in the Bela Board Settings\nsection. After connecing the Bela Board to computer via USB make sure you the drive is visible in My Computer'
cfgM_infonote = customtkinter.CTkLabel(configFrameMain, text= cfgM_infonotestr, font=B3, text_color= '#5f5f5f', justify= 'left')
cfgM_infonote.grid(row=8, column=0, columnspan= 10, sticky='w', padx= (40,0), pady= (24,0))

# back button
cfgM_BTback2main = customtkinter.CTkButton(configFrameMain, text= 'Back to Main Menu', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f', 
                                 command= on_cfgmsave)
cfgM_BTback2main.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))
# save button
cfgM_BTsave = customtkinter.CTkButton(configFrameMain, text= 'Save Changes',
                                    command= on_cfgsave)
cfgM_BTsave.grid(row=9, column=9, sticky='se', padx= (10,40), pady= (0,40))




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

