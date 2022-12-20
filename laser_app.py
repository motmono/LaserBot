# This is a python app to be run on a raspberry pi that will allow for control of robot.
# The robot will be setup to connect to the home network and the pi will be setup to be remoted into.
# Code written by: Tom Van Noord

# Project expansion to include dog recognition via rpi camera and email/sms control

# Coordinates will be written as X, Y, Time

from operator import truediv
import tkinter as tk
from tkinter import ttk
from turtle import bgcolor
import serial
import socket
import struct
import time
import re

IP = "16.103.106.25" #IP address of robot after connected to home network
PORT = 2222
IN_PORT = 2223
LaserPointerSock = None

# Tkinter app code
app = tk.Tk()
app.title("Laser Robot App")
app.geometry("750x650")

frame_background = tk.Frame(app).pack(expand=True)
tk.Label(frame_background, text="testing frame background text").pack(side=tk.TOP)


# Robot control buttons
# Create an internal frame that can contain all the control buttons
button_frame = tk.Frame(frame_background).pack(expand=True)

tk.Label(button_frame, text="Robot Control: Press buttons to move robot to teach points!").place(relx=0.5, y=10, anchor=tk.CENTER)
tk.Button(button_frame, text="Up", command=app.destroy).place(relx=0.5, y=100, anchor=tk.CENTER)
tk.Button(button_frame, text="Left", command=app.destroy).place(x=5, y=45)
tk.Button(button_frame, text="Right", command=app.destroy).place(x=95, y=45)
tk.Button(button_frame, text="Down", command=app.destroy).place(relx=0.5, y=75, anchor=tk.CENTER)
#tk.Button(button_frame, text="Up", command=app.destroy).pack()
#tk.Button(button_frame, text="Left", command=app.destroy).pack()
#tk.Button(button_frame, text="Right", command=app.destroy).pack()
#tk.Button(button_frame, text="Down", command=app.destroy).pack()

#frame_background.pack(side='top')
#button_frame.pack(expand=True)

quit_frame = tk.Frame(frame_background).pack(side=tk.BOTTOM)
tk.Button(quit_frame, text="Quit", command=app.destroy).pack()



app.mainloop()
