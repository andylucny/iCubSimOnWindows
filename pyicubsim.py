# developed by Andrej Lucny from Comenius University in Bratislava, www.agentspace.org/andy

# for Python >= 3.8 which ignores %PATH%
import sys
import os
if sys.version >= '3.8':
    os.add_dll_directory(os.path.abspath(os.path.curdir)+'/iCubSim/bin') 

import yarp
import numpy as np
import cv2
import socket
import re
import time

class NoYarp:
    # parse respose from naming service
    @staticmethod
    def get_addr(s):
        m = re.match("registration name [^ ]+ ip ([^ ]+) port ([0-9]+) type tcp",s)
        return (m.group(1),int(m.group(2))) if m else None
    # get a single line of text from a socket
    @staticmethod
    def getline(sock):
        result = ""
        while result.find('\n')==-1:
            result = result + sock.recv(1024).decode()
        result = re.sub('[\r\n].*','',result)
        return result
    # send a message and expect a reply
    @staticmethod
    def command(addr,message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(addr)
        sock.send('CONNECT extern\n'.encode())
        NoYarp.getline(sock) 
        if isinstance(message, tuple):
            result=()
            for command in message:
                #print('SENT: ',command);
                sock.send(('d\n%s\n' % command).encode())
                result += (NoYarp.getline(sock),)
                #print('RECEIVED: ',result[-1]);
        else:
            sock.send(('d\n%s\n' % message).encode())
            result = NoYarp.getline(sock)
        sock.close()
        return result
    # call YARP naming service
    @staticmethod
    def query(host, port_name):
        return NoYarp.get_addr(NoYarp.command((host,10000),"query %s"%port_name))

class Yarp:
    initialized = False
    @staticmethod
    def initialize():
        if not Yarp.initialized:
            yarp.Network.init()
            time.sleep(0.1)
            Yarp.initialized = True
            print('Yarp initialized')
    
class iCubLimb:
    def __init__(self,app_name,port_name):
        Yarp.initialize()
        # prepare a property object
        self.props = yarp.Property()
        self.props.put('device','remote_controlboard')
        self.props.put('local',app_name+port_name)
        self.props.put('remote',port_name)
        # create remote driver
        self.armDriver = yarp.PolyDriver(self.props)
        # query motor control interfaces
        self.iPos = self.armDriver.viewIPositionControl()
        #self.iVel = self.armDriver.viewIVelocityControl()
        self.iEnc = self.armDriver.viewIEncoders()
        # retrieve number of joints
        self.jnts = self.iPos.getAxes()
        time.sleep(0.1)
        print('Controlling', self.jnts, 'joints of', port_name)
        
    def get(self):
        # read encoders
        encs = yarp.Vector(self.jnts)
        self.iEnc.getEncoders(encs.data())
        values = ()
        for i in range(self.jnts):
            values += (encs.get(i),)
        return values
        
    def set(self,values=(), \
        joint0=None,joint1=None,joint2=None,joint3=None,joint4=None,joint5=None,joint6=None,joint7=None, \
        joint8=None,joint9=None,joint10=None,joint11=None,joint12=None,joint13=None,joint14=None,joint15=None):
        # read encoders
        encs = yarp.Vector(self.jnts)
        self.iEnc.getEncoders(encs.data())
        # adjust joint positions
        for i in range(min(self.jnts,len(values))):
            if values[i] != None:
                encs.set(i,values[i])
        for i in range(16):
            value = eval('joint'+str(i))
            if value != None:
                print('joint',i,'=',value)
                encs.set(i,value)
        # write to motors
        self.iPos.positionMove(encs.data())
        
    def size(self):
        # return number of joints
        return self.jnts

class iCubCamera:
    def __init__(self,app_name,port_name):
        Yarp.initialize()
        # open recipient port
        self.port = yarp.Port()
        self.port.open(app_name+port_name)
        yarp.delay(0.25)
        # connect the port to camera
        yarp.Network.connect(port_name,app_name+port_name)
        yarp.delay(0.25)
        # prepare data buffer for reception
        self.width = 320
        self.height = 240
        self.yarp_img = yarp.ImageRgb()
        self.yarp_img.resize(self.width,self.height)
        self.array_img = bytearray(self.width*self.height*3)
        self.yarp_img.setExternal(self.array_img,self.width,self.height)
        # prepare blank image to be returned when an error appears
        self.blank = np.zeros(self.shape())

    def grab(self):
        # receive one image
        self.port.read(self.yarp_img)
        # check if the image is correct
        if self.yarp_img.height() == self.height and self.yarp_img.width() == self.width:
            # turn the image to openCV format
            img = np.frombuffer(self.array_img, dtype=np.uint8)
            img = img.reshape(self.height,self.width,3)
            # correct its color model
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # return the OpenCV image
            return img
        else:
            return blank

    def shape(self): # can be called before any image is received
        # return shape of image provided by this camera 
        return (self.height,self.width,3)

class iCubEmotion:
    def __init__(self):
        host = 'localhost' #'192.168.56.1'
        port_name = '/emotion/in'
        self.query = NoYarp.query(host,port_name)
        self.neutral = 'neu'
        self.happy = 'hap'
        self.sad = 'sad'
        self.surprised = 'sur'
        self.angry = 'ang'
        self.evil = 'evi'
        self.shy = 'shy'
        self.cunning = 'cun'
        self.set(self.neutral)

    def set(self, emotion='neu'):
        commands = ('set all '+emotion,)
        NoYarp.command(self.query,commands)

class iCubBall:
    def __init__(self):
        host = 'localhost' #'192.168.56.1'
        port_name = '/icubSim/world'
        self.query = NoYarp.query(host, port_name)
        self.get()
        
    def get(self):
        commands = ('world get ball',)
        response = NoYarp.command(self.query,commands)
        values = response[0].split()
        self.x = float(values[0])
        self.y = float(values[1])
        self.z = float(values[2])
        return self.x, self.y, self.z

    def set(self, x=None, y=None, z=None):
        if x is None and y is None and z is None:
            x = -0.15
            y = 0.5539755
            z = 0.35
        if x is None or y is None or z is None:
            self.get()
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
        commands = ('world set ball '+str(self.x)+' '+str(self.y)+' '+str(self.z),)
        NoYarp.command(self.query,commands)
    
    def setDefault(self):
        self.set()

