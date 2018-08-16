from PyQt4 import QtGui ,QtCore
import sys
from PyQt4.Qt import QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout,\
    QDialog, QBoxLayout, QMenuBar, QFileDialog
import matplotlib.pyplot as plt
from fileinput import filename
import csv

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        ##Creating and new window
        self.win1=QtGui.QWidget()
        self.win1.setGeometry(10,20,300,100)
        self.win1.setWindowTitle("Data_LOG Plotter")
        self.win1.setFixedWidth(300)
        
        ## Setting for the vertical layout##
        layout1=QVBoxLayout()
        
        ## Adding buttons and stuffs##     ## In Layout format button.resize and button.move won't work      
        self.line_edit=QLineEdit()
        button=QPushButton("Browse")
        button2=QPushButton("Read")
        button3=QPushButton("Exit Application")
        
        ##Adding widgets in layout structure##
        layout1.addWidget(self.line_edit)
        layout1.addWidget(button)
        layout1.addWidget(button2)
        layout1.addWidget(button3)
        ##Showing layout items
        self.win1.setLayout(layout1)
        
        ##Showing the the current window
        self.win1.show()
        
        button.clicked.connect(self.browse)
        button2.clicked.connect(self.read_file)
        button3.clicked.connect(self.win1.close)
        
    def browse(self):
        self.save_file=QFileDialog.getOpenFileName(self, caption="Read File As",filter="Comma Separated Variable(*.csv*)")
        self.line_edit.setText(self.save_file)
        
    
    def read_file(self):
        ##Creating empty Data Array
        data_array=[]
        with open(self.save_file,'rb') as f:
            reader=csv.reader(f)
            for row in reader:
                content=row[1]
                data_array.append(content)
            
            plt.plot(data_array)
            plt.show()
app=QtGui.QApplication(sys.argv)
GUI=Window()
sys.exit(app.exec_())
