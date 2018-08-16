### Importing all the Libraries
import serial
import serial.tools.list_ports
from PyQt4 import QtGui, QtCore
from pyqtgraph.Qt import QtGui,QtCore
import pyqtgraph as pg
import sys
import time
from PyQt4.Qt import QComboBox, QPushButton
from serial.tools.list_ports_windows import Ports

### Creating a class
class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        ## Creating my 1st window
        self.win1=QtGui.QWidget()
        self.win1.resize(300,100)
        
        self.win1.setWindowTitle("DATA AQUISITION")
        ##Creating a vertical layout
        layout1=QtGui.QGridLayout()
        combobox1=QtGui.QComboBox()
        connect_button=QtGui.QPushButton("Connect")
        close_button=QtGui.QPushButton("Disconnect")
        label_comport=QtGui.QLabel("Choose Comport")
        exit_button=QtGui.QPushButton("Exit")
            
        
        ##Adding widgets to layout
        layout1.addWidget(label_comport,0,0)
        layout1.addWidget(combobox1,1,0)
        layout1.addWidget(connect_button,1,1)
        layout1.addWidget(close_button,2,0)
        layout1.addWidget(exit_button,2,1)
        
        ##Showing widget
        self.win1.setLayout(layout1)
        ##Showing the window
        self.win1.show()
        ## Making button events
        exit_button.clicked.connect(self.win1.close)
        

app=QtGui.QApplication(sys.argv)
GUI=Window()
sys.exit(app.exec_())