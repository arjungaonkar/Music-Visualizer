from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import  random
import math

from threading import Thread
import pyaudio, wave
import numpy as np
from pyglet.gl import GL_POINTS
from scipy.fftpack import fft
import  time

Frequencies=[0]

class Music(Thread):
    def __init__(self,filepath):
        self.filepath=filepath
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        CHUNK = 1024 * 4
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        wf = wave.open(self.filepath, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(), rate=wf.getframerate(), input=True,
                        output=True, frames_per_buffer=1024)
        files_seconds = wf.getnframes() / RATE
        x = np.arange(0, 16 * CHUNK, 8)
        x_fft = np.linspace(0, RATE, CHUNK)
        frame_count = 0
        start_time = time.time()
        global Frequencies
        while True:
            data = wf.readframes(CHUNK)
            data_int = np.fromstring(data, dtype=np.int16)
            y_fft = fft(data_int)
            abs_y_fft = np.abs(y_fft[0:CHUNK]) * 2 / (10000 * CHUNK)
            Frequencies=abs_y_fft
            try:
                stream.write(data)
                frame_count = frame_count + 1
            except:
                frame_rate = frame_count / (time.time() - start_time)
                print("stream stopped")
                print('average frame rate = {:.0f} FPS'.format(frame_rate))
                break

class Point:
    def __init__(self,x,y,z=None):
        self.x=x
        self.y=y
        if(z==None):
            self.z=0
        else:
            self.z=z


SpherePoint=[]
Angel1=45
Angel2=0
def map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

def clamp(myValue, minValue, maxValue):
    return max(min(myValue, maxValue), minValue)

def calculateSphere(r,n):
    for i in range(n):
        lon=map(i,0,n,-math.pi,math.pi)

        row=[]
        for j in range(n):
            lat = map(j, 0, n, -math.pi, math.pi)
            x = r * math.sin(lon) * math.cos(lat)
            y = r * math.sin(lon) * math.sin(lat)
            z = r * math.cos(lon)

            p=Point(x,y,z)
            row.append(p)
        SpherePoint.append(row)

def rotateup():
    global Angel1
    Angel1=Angel1+1

def rotatedown():
    global Angel1
    Angel1=Angel1-1

def rotateright():
    global Angel2
    Angel2 = Angel2 + 1

def rotateleft():
    global Angel2
    Angel2 = Angel2 - 1

n=100

calculateSphere(0.5,n)

def initGL():
    glClearColor(1.0,1.0,1.0,1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-250,250,-250,250)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    global Angel1,Frequencies

    n = Frequencies[0]*100
    d = 0.97

    glPointSize(2)
    glBegin(GL_POINTS)
    for i in range(361):
        k = i * d
        r = 0.7 * math.sin(n * k)
        x = r * math.sin(k)
        y = r * math.cos(k)
        rgb = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
        glColor(rgb)
        glVertex2f(x, y)
    glEnd()




    glFlush()

LeftClick=False
PreviuosPoint=Point(0,0)

def mouseClick(button,state,x,y):
    global LeftClick,IntialPoint
    if(button==0 and state==0):
        IntialPoint=Point(x,y)
        LeftClick=True
    elif(button==0 and state==1):
        LeftClick = False

def mouseMotion(x,y):
    if(LeftClick):
        global PreviuosPoint
        Distance=Point(x-IntialPoint.x,y-IntialPoint.y)
        if(abs(Distance.x)>abs(Distance.y)):
            if(Distance.x>PreviuosPoint.x):
                print("Right")
                rotateright()
            else:
                print("Left")
                rotateleft()
        else:
            if (Distance.y<PreviuosPoint.y):
                print("Up")
                rotateup()
            else:
                print("Down")
                rotatedown()
        PreviuosPoint=Distance

glutInit()
glutInitWindowSize(750,750)
glutCreateWindow(b"Music Visualizer")
glutDisplayFunc(display)
glutIdleFunc(display)
glutMouseFunc(mouseClick)
glutMotionFunc(mouseMotion)
Music("ukiyo.wav")
glutMainLoop()
