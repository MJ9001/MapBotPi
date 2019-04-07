import serial

from serial_cfg import *

class MotorDriverInterface:
    def __init__(self):
        self.port = serial.Serial(MOTOR_DRIVER_PORT, BAUD_RATE)
        self.setMotionAllowed(True)
        self.setTargetVelocities(10, 10)

    def __del__(self):
        self.setMotionAllowed(False)

    def debugWrite(self, s):
        self.port.write(s)
        print(s)

    def setMotionAllowed(self, value):
        if value is True:
            self.port.write(b"[setMotionAllowed=1]")
        else:
            self.port.write(b"[setMotionAllowed=0]")

    def stop(self):
        self.port.write(b"[stop=0]")

    def setTargetVelocities(self, x=None, y=None, a=None):
        if x is not None:
            self.port.write(b"[setCommandX=" + str(x).encode('ascii') + b"]")
        if y is not None:
            self.port.write(b"[setCommandY=" + str(y).encode('ascii') + b"]")
        if a is not None:
            self.port.write(b"[setCommandA=" + str(a).encode('ascii') + b"]")
        self.port.write(b"[setTargetVelocities=0]")  

    def setMaxVelocities(self, x=None, y=None, a=None):
        if x is not None:
            self.port.write(b"[setCommandX=" + str(x).encode('ascii') + b"]")
        if y is not None:
            self.port.write(b"[setCommandY=" + str(y).encode('ascii') + b"]")
        if a is not None:
            self.port.write(b"[setCommandA=" + str(a).encode('ascii') + b"]")
        self.port.write(b"[setMaxVelocities=0]") 
        
    def setMaxAccelerations(self, x=None, y=None, a=None):
        if x is not None:
            self.port.write(b"[setCommandX=" + str(x).encode('ascii') + b"]")
        if y is not None:
            self.port.write(b"[setCommandY=" + str(y).encode('ascii') + b"]")
        if a is not None:
            self.port.write(b"[setCommandA=" + str(a).encode('ascii') + b"]")
        self.port.write(b"[setMaxAccelerations=0]")     

    def setMicrostepping(self, step):
        self.port.write(b"[setMicrostepping=" + str(step & 0xFF) + b"]")

    def gotoXYA(self, x=None, y=None, a=None):
        if x is not None:
            self.port.write(b"[setCommandX=" + str(x).encode('ascii') + b"]")
        if y is not None:
            self.port.write(b"[setCommandY=" + str(y).encode('ascii') + b"]")
        if a is not None:
            self.port.write(b"[setCommandA=" + str(a).encode('ascii') + b"]")
        self.port.write(b"[gotoXYA=0]")

    def gotoXY(self, x=None, y=None, a=None):
        if x is not None:
            self.port.write(b"[setCommandX=" + str(x).encode('ascii') + b"]")
        if y is not None:
            self.port.write(b"[setCommandY=" + str(y).encode('ascii') + b"]")
        self.port.write(b"[gotoXY=0]")  

    def moveFR(self, f=None, r=None):
        if f is not None:
            self.debugWrite(b"[setCommandX=" + str(f).encode('ascii') + b"]")
        if r is not None:
            self.debugWrite(b"[setCommandY=" + str(r).encode('ascii') + b"]")
        self.debugWrite(b"[moveFR=0]")

    def rotateTo(self, theta):
        self.port.write(b"[rotateTo=" + str(theta).encode('ascii') + b"]")

    def rotate(self, theta):  
        self.port.write(b"[rotate=" + str(theta).encode('ascii') + b"]")

    def resetPosition(self, x=None, y=None, a=None):
        if x is not None:
            self.port.write(b"[setCommandX=" + str(x).encode('ascii') + b"]")
        if y is not None:
            self.port.write(b"[setCommandY=" + str(y).encode('ascii') + b"]")
        if a is not None:
            self.port.write(b"[setCommandA=" + str(a).encode('ascii') + b"]")
        self.port.write(b"[resetPosition=0]")
        print(self.port.readline())