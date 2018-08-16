### Importing all the Libraries
import serial
import serial.tools.list_ports
from PyQt4 import QtGui, QtCore
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import time
from PyQt4.Qt import QComboBox, QPushButton
from serial.tools.list_ports_windows import Ports
from pykeyboard import PyKeyboard
from pymouse import  PyMouse
from serial.serialutil import SerialException
from pyqtgraph.widgets.ColorButton import ColorButton
import threading
from queue import Queue
from collections import deque
import collections
import numpy as np
import csv
from datetime import datetime
from numpy import empty


m=PyMouse()
print m.screen_size()
### Creating a class
class Window(QtGui.QMainWindow):
    global i
    i=0
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        ## Creating my 1st window
        self.win1 = QtGui.QWidget()
        self.win1.resize(300, 100)

        self.win1.setWindowTitle("DATA AQUISITION")
        ##Creating a vertical layout
        layout1 = QtGui.QGridLayout()
        self.combobox1 = QtGui.QComboBox()
        self.combobox2 = QtGui.QComboBox()
        self.connect_button = QtGui.QPushButton("Connect")
        label_comport = QtGui.QLabel("Choose Comport")
        exit_button = QtGui.QPushButton("Exit")
        label_baud=QtGui.QLabel("Buad Rate")
        ## Adding list to comports
        available=[]
        for i in range(256):
            try:
                y='COM'+str(i)
                sdr=serial.Serial(y,9600)
                sdr.close()
                print y
                available.append(y)
            except SerialException:
                pass
            
        self.combobox1.addItems(available)
        self.combobox1.currentIndexChanged.connect(self.select)
        self.combobox2.addItems(["4800","9600","115200"])



        ##Adding widgets to layout
        layout1.addWidget(label_comport, 0, 0)
        layout1.addWidget(label_baud,0,1)
        layout1.addWidget(self.combobox1, 1, 0)
        layout1.addWidget(self.combobox2,1,1)
        layout1.addWidget(self.connect_button, 2, 0)
        layout1.addWidget(exit_button, 2, 1)

        ##Showing widget
        self.win1.setLayout(layout1)
        ##Showing the window
        self.win1.show()
        ## Making button events
        exit_button.clicked.connect(self.win1.close)
        self.connect_button.clicked.connect(self.connected)



        ## Creating an another plot file
        self.win2=QtGui.QWidget()
        
        ##
        self.plot1=pg.PlotWidget()
        plot2=pg.PlotWidget()
        plot3=pg.PlotWidget()
        plot4=pg.PlotWidget()
        ##
        
        #self.plot1.showGrid(x=True,y=True,alpha=None)
        
        ## Just an example for plotting
        '''
        p1=[1,2,3]
        plot1.plot(p1)
        p2=[2,3,4]
        plot1.plot(p2,pen=(255,0,0))
       '''
        
        
        ##Make room for buttons
        self.plot1_button_start=QtGui.QPushButton("Plot 1 Start")
        self.plot1_button_stop=QtGui.QPushButton("Plot 1 Stop")
        plot2_button_start=QtGui.QPushButton("Plot 2 Start")
        plot2_button_stop=QtGui.QPushButton("Plot 2 Stop")
        plot3_button_start=QtGui.QPushButton("Plot 3 Start")
        plot3_button_stop=QtGui.QPushButton("Plot 3 Stop")
        plot4_button_start=QtGui.QPushButton("Plot 4 Start")
        plot4_button_stop=QtGui.QPushButton("Plot 4 Stop")
        play_all=QtGui.QPushButton("Play All")
        stop_all=QtGui.QPushButton("Stop All")
        slider=QtGui.QSlider(QtCore.Qt.Horizontal)
        drv_str=QtGui.QLabel("Steering position")
        acc=QtGui.QLabel("Acceleration")
        
    
        ##Making Grid_Layout and adding widgets to Layout        
        layout2=QtGui.QGridLayout()
        
        
        
        layout2.addWidget(self.plot1,0,0,4,4)
        layout2.addWidget(self.plot1_button_start,6,0)
        self.plot1_button_start.setFixedWidth(150)
        layout2.addWidget(self.plot1_button_stop,6,1)
        self.plot1_button_stop.setFixedWidth(150)
        
        
        layout2.addWidget(plot2,0,4,4,4)
        layout2.addWidget(plot2_button_start,6,4)
        layout2.addWidget(plot2_button_stop,6,5)
        
        
        layout2.addWidget(plot3,8,0,4,4)
        layout2.addWidget(plot3_button_start,12,0)
        plot3_button_start.setFixedWidth(150)
        layout2.addWidget(plot3_button_stop,12,1)
        plot3_button_stop.setFixedWidth(150)
        
        layout2.addWidget(plot4,8,4,4,4)
        layout2.addWidget(plot4_button_start,12,4)
        layout2.addWidget(plot4_button_stop,12,5)
        
        
        layout2.addWidget(play_all)
        layout2.addWidget(stop_all)
        
        
        layout2.addWidget(drv_str,13,0)
        
        layout2.addWidget(slider,13,1)
        
        ##Slider Settings
        slider.setMaximum(360)
        slider.setFixedWidth(500)
        slider.setSliderPosition(180)
        print slider.sliderPosition() ##For Debugging proposes
        
        
        
        ##Adding color to button
        play_all.setStyleSheet("background-color: green")
        stop_all.setStyleSheet("background-color: red")
        
        self.win2.setLayout(layout2)
        
    
        
        ## Adding Timer for plot1 and other
        self.timer=QtCore.QTimer()
        self.accx=[]
        self.accx2=[]
        self.accx3=[]
        self.j=0
        self.plot1_button_start.clicked.connect(self.plot1_timer)
        self.plot1_button_stop.clicked.connect(self.plot1_stop)
        self.k=0
        ## Creating csv object
        self.csvfile=open("data.csv","w")
        self.writer=csv.writer(self.csvfile)
        
    def plot1_timer(self):
        self.timer.timeout.connect(self.plot1_update)
        self.timer.start(250)
    
    def plot1_stop(self):
        self.timer.stop()
        self.csvfile.close()                #Temporary program,Remove it after being completion of program
    
    def select(self):
        index=self.combobox1.currentText()
        print index

    def connected(self):
        global i
        if(i==0):
            self.connect_button.setText("Disconnect")
            print self.combobox1.currentText()
            print self.combobox2.currentText()
            if self.combobox1.currentText()!="":
                try:
                    
                    self.sdr=serial.Serial(str(self.combobox1.currentText()),int(self.combobox2.currentText()),timeout=.1)
                except:
                    SerialException()
                    pass
                
            self.win2.showMaximized()
            self.win1.hide()
            i=i+1
        elif (i==1):
            self.connect_button.setText("Connect")
            self.sdr.close()
            i=0
            print "Disconnected"

        
        
     ## Plot Function
    def plot1_update(self):   
        
        data=self.sdr.readline()
        if(data!=""):
            
            data.split(',')
            data1=float(data[0])
            print data1
            self.accx.append(data1)
            data2=float(data[1])
            print 
            self.accx2.append(data2)
            data3=float(data[2])
            self.accx3.append(data3)
            
            self.plot1.plot(self.accx,pen=(255,0,0))
        
        print self.j
        print self.accx  
        app.processEvents()
        
        
        

app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())