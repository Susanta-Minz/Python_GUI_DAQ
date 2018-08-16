### Importing all the Libraries
import serial
import serial.tools.list_ports
from PyQt4 import QtGui, QtCore
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import time
from PyQt4.Qt import QComboBox, QPushButton ,QFileDialog
from serial.tools.list_ports_windows import Ports
from pykeyboard import PyKeyboard
from pymouse import  PyMouse
from serial.serialutil import SerialException
from pyqtgraph.widgets.ColorButton import ColorButton
from queue import Queue
from collections import deque
import collections
import numpy as np
import csv
from datetime import datetime
from numpy import empty
import matplotlib.pyplot as plt
from matplotlib import style


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
        self.win1.setFixedWidth(300)
        self.win1.setFixedHeight(125)
        
        self.win1.setWindowTitle("DATA AQUISITION")
        ##Creating a vertical layout
        layout1 = QtGui.QGridLayout()
        self.combobox1 = QtGui.QComboBox()
        self.combobox2 = QtGui.QComboBox()
        self.connect_button = QtGui.QPushButton("Connect")
        label_comport = QtGui.QLabel("Choose Comport")
        exit_button = QtGui.QPushButton("Exit")
        label_baud=QtGui.QLabel("Buad Rate")
        browse_button=QtGui.QPushButton("Browse")
        read_button=QtGui.QPushButton("Read")
        
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
        layout1.addWidget(browse_button, 2, 0)
        layout1.addWidget(read_button, 2, 1)
        layout1.addWidget(self.connect_button,3,0)
        layout1.addWidget(exit_button,3,1)

        ##Showing widget
        self.win1.setLayout(layout1)
        ##Showing the window
        self.win1.show()
        ## Making button events
        exit_button.clicked.connect(self.win1.close)
        self.connect_button.clicked.connect(self.connected)

        browse_button.clicked.connect(self.browse)
        read_button.clicked.connect(self.read_file)

        ## Creating an another plot file
        self.win2=QtGui.QWidget()
        
        ##
        self.plot1=pg.PlotWidget()
        #self.plot1.setYRange(-10,10) #Set for the Y Range
       # self.plot1.setXRange(0,30,padding=0,update=True)
       # self.plot1.setYRange(-2,10, padding=0,update=True)
        self.plot2=pg.PlotWidget()
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
        
        
        layout2.addWidget(self.plot2,0,4,4,4)
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
        self.k=1
        self.z=0
        self.temp_array=[]
        self.plot1_button_start.clicked.connect(self.plot1_timer)
        self.plot1_button_stop.clicked.connect(self.plot1_stop)
        
        
    def plot1_timer(self):
        self.timer.timeout.connect(self.plot1_update)
        self.timer.start(1)
    
    def plot1_stop(self):
        self.timer.stop()
        self.csvfile.close() 
        self.win2.close()              
          
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
                    ## Creating csv object
                    time_stamp=time.strftime('%Y-%m-%d-%H-%M-%S')
                    time_stamp_file=str(time_stamp)+".csv"
                    self.csvfile=open(time_stamp_file,"wb")
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

        
    ## For Browsing File
    def browse(self):
        self.read_file=QFileDialog.getOpenFileName(self, caption="Read File As",filter="Comma Separated Variable(*.csv*)")
      
      
    ## For Reading the browsed file
    def read_file(self):
        ##Creating empty Data Array
        data_acc_x=[]
        data_temp=[]
        
        ##Creating Subplots
        fig=plt.figure()
        fig.suptitle("TEAM ROADRUNNER")
        
        ax1=fig.add_subplot(221)
        ax1.set_title('Acceleration')
        ax1.set_ylabel('g')
        
        ax2=fig.add_subplot(222)
        ax2.set_title("Temperature")
        ax2.set_ylabel('Celsius')
        
        ax3=fig.add_subplot(223)
        ax3.set_title("Throttle Position(%)")
        
        ax4=fig.add_subplot(224)
        ax4.set_title("Wheel RPM")
        
        with open(self.read_file,'rb') as f:
            reader=csv.reader(f)
            for row in reader:
                acc_x=row[0]
                temp=row[1]
                data_acc_x.append(acc_x)
                data_temp.append(temp)
        print data_acc_x
        print data_temp    
        ax1.plot(data_acc_x)
        ax2.plot(data_temp)
        plt.show()
      
      
     ## Plot Function
    def plot1_update(self):   
        
        data=self.sdr.readline()
        print data
        if(data!=""):
            
            dt=datetime.now()
            a,b,c=data.split(",")
            
            
            self.writer=csv.writer(self.csvfile)
            self.writer.writerow([float(a),float(b)])
            self.accx.append(float(a))
            self.temp_array.append(float(b))
            self.plot1.clear()
            self.plot2.clear()
            self.plot1.plotItem.plot(self.accx)
            self.plot2.plotItem.plot(self.temp_array)
            if(self.j>=100):
                self.accx.pop(0)
                self.temp_array.pop(0)
                self.j=102
            self.j=self.j+1
        app.processEvents()
        
        
        

app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
