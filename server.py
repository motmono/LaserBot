from flask import Flask, render_template

import struct
import socket
import time
import random
from threading import Event

# Create a threaded event for our robot motion
exit = Event()

# Variables for Wifi connection:
IP = "A FREE IP ADDRESS ON YOUR NETWORK" # Default ROBOT IP
PORT = 2222        # Default ROBOT port
IN_PORT = 2223     # Default ROBOT input port
LaserPointerSock = None

def sendCommand(Header,p1,p2,p3=0,p4=0,p5=0,p6=0,p7=0,p8=0):
    base = bytearray(Header)  # message
    param1 = bytearray(struct.pack(">h",p1))
    param2 = bytearray(struct.pack(">h",p2))
    param3 = bytearray(struct.pack(">h",p3))
    param4 = bytearray(struct.pack(">h",p4))
    param5 = bytearray(struct.pack(">h",p5))
    param6 = bytearray(struct.pack(">h",p6))
    param7 = bytearray(struct.pack(">h",p7))
    param8 = bytearray(struct.pack(">h",p8))
    message = base+param1+param2+param3+param4+param5+param6+param7+param8
    print(message)

    try:
        LaserPointerSock.sendto(message,(IP,PORT))
    except:
        print("Could not send message (Wifi)!")

def sendAngles(new_a1,new_a2):
    global a1,a2
    try:
        #print("a1:",a1,"a2:",a2)
        a1 = new_a1
        a2 = new_a2
        sendCommand(b'JJAM',int(a1*100),int(a2*100))
    except:
        print("Error!")

def sendAngles2(new_a1,new_a2,s=0.5):
    global a1,a2
    try:
    #print("a1:",a1,"a2:",a2)
        a1 = new_a1
        a2 = new_a2
        sendCommand(b'JJAM',int(a1*100),int(a2*100))
        exit.wait(s)
    except:
        print("Error!")

def downstairs():
    first = 0
    last = 0
    while not exit.is_set():
        order = random.sample(range(1,5),4)
        first = order[0]
        print(order)
        if first != last: 
            for i in order:
                t=random.randint(3,5)
                if i == 1:
                    sendAngles2(0,-16,2)
                elif i == 2:
                    sendAngles2(80,-52,t)
                elif i == 3:
                    sendAngles2(-77,-91,t)
                elif i == 4:
                    adjust=random.randint(1,7)
                    angle=-80+adjust
                    sendAngles2(-45,angle,2)
        last = order[3]

    print("Exited program!")
    exit.clear()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/on/')
def turn_laser_on():
    print("turning on laser")
    sendCommand(b'JJON',0,0,0,0,0,0,0,0)

    return 'Laser on. Go back to Home'

@app.route('/off/')
def turn_laser_off():
    print("turning off laser")
    sendCommand(b'JJOF',0,0,0,0,0,0,0,0)

    return 'Laser off. Go back to Home'

@app.route('/startprog/')
def start_robot():
    print("Starting Robot")
    downstairs()
    return 'Robot running. Go back to Home'

@app.route('/stopprog/')
def stop_robot():
    print("Stopping Robot")
    exit.set()
    time.sleep(2)
    sendAngles(0,0)
    return 'Robot stopping. Go back to Home'

@app.route('/reconnect/')
def reconnect_robot():
    print("Reconnecting to robot!")
    try:
        print("Opening socket...")
        LaserPointerSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        LaserPointerSock.sendto(b'JJAH0000000000000000',(IP,PORT))
        sendCommand(b'JJAS',50,0,70,0) # 50% speed, 70% accel
        return "Connected to Laser Pointer via Wifi... "        
    except:
        return "Could not connect to laser pointer!"


if __name__ == '__main__':
    try:
        print("Opening socket...")
        LaserPointerSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        LaserPointerSock.sendto(b'JJAH0000000000000000',(IP,PORT))
        print("Connected to Laser Pointer via Wifi... ")
    except:
        print("! Could not connect to laser pointer!. Check you are connected to the robot Wifi network (JJROBOTS_xx)")

    sendCommand(b'JJAS',50,0,70,0) # 50% speed, 70% accel

    app.run(host='0.0.0.0', port=8080 ,debug=True)