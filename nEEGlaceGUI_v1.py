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


# system settings 
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

# app frame
app = customtkinter.CTk()
app.geometry('720x480')
app.title('nEEGlace GUI')

# font styles 
H1 = ('Arial', 24, 'bold')
B1 = ('Arial', 14)

for i in range(10): 
    app.grid_rowconfigure(i, weight=1 if i == 9 else 0)
    app.grid_columnconfigure(i, weight=1 if i == 9 else 0)

# # adding mainwindow UI
# # main title 
title = customtkinter.CTkLabel(app, text= 'Welcome to nEEGlace', font=H1)
title.grid(row=0, column=0, sticky='w', padx= (40,0), pady= (40,0))
# body text 
bodystr = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor\nincididunt ut labore et dolore magna aliqua.'
body = customtkinter.CTkLabel(app, text= bodystr, font=B1, text_color='#979797', justify= 'left')
body.grid(row=2, column=0, sticky='w', padx= (40,0), pady= (10,0))

# bottom buttons
BTtroubleshoot = customtkinter.CTkButton(app, text= 'Troubleshoot', fg_color='#5b5b5b', text_color='#b6b6b6', hover_color='#4f4f4f')
BTtroubleshoot.grid(row=9, column=0, sticky='sw', padx= (40,0), pady= (0,40))
# bottom buttons
BTsetup = customtkinter.CTkButton(app, text= 'Setup nEEGlace', fg_color='#ffffff', text_color='#000000', hover_color='#979797')
BTsetup.grid(row=9, column=1, sticky='sw', padx= (0,0), pady= (0,40))
# bottom buttons
BTstart = customtkinter.CTkButton(app, text= 'Start Recording')
BTstart.grid(row=9, column=9, sticky='se', padx= (0,0), pady= (0,40))


# run app
app.mainloop()

