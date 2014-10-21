'''
Created on 21 Oct 2014

    Copyright (c) 2014 Brendan Gray and Sylvermyst Technologies

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    
'''


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QTimer

from Slapt.constants import *


class MainScreen(QtGui.QMainWindow):
    
    def __init__(self):

        super(MainScreen, self).__init__() # Call the constructor of this class's parent        
        self.prepare()
        self.loadSettings()
        
        self.initUI()
        
        self.fpsTimer = QTimer()
        self.fpsTimer.timeout.connect(self.updateDisplay)
        self.fpsTimer.start(1000/targetFPS) # set targetFPS in constants.
        
    def prepare(self):
        '''
        Initialises variables that need to be set before the GUI is initialised.
        '''
        
        pass
        
    
    def updateDisplay(self):
        '''
        Updates the display
        '''
        
        
                
                

            
            
   
        pass
    
    
    def keyPressEvent(self, event):
        '''
        Handles key presses anywhere in the program.
        '''
        
        if event.key() in [Qt.Key_Control, Qt.Key_Meta]: # Either a Ctrl key in Windows and Linux, or the Command key of a Mac
            if int(event.nativeScanCode()) < 80:
                # This is a messy work around, and may not always work.
                # scan code gave 25 and 285 on my Windows 7 machine, and 37 and 105 on my Ubuntu machine for L and R Ctrl respectively.
                # It would be better if Qt could tell L and R Ctrl apart, but it seems that it can't. 
                print("Left Ctrl pressed")
            else:
                print("Right Ctrl pressed")

    
    def keyReleaseEvent(self, event):
        '''
        Handles key presses anywhere in the program.
        '''
        
        keyScanCode = event.nativeScanCode()
        if event.key() in [Qt.Key_Control, Qt.Key_Meta]: # Either a Ctrl key in Windows and Linux, or the Command key of a Mac
            if int(event.nativeScanCode()) < 80:
                # This is a messy work around, and I'm not sure it will always work.
                print("Left Ctrl released",int(event.nativeScanCode()))
            else:
                print("Right Ctrl released",int(event.nativeScanCode()))
            
            
             
        
    def initUI(self):
        '''
        Initialises the UI layout and widgets.
        '''
        
        timerWindow = QtGui.QWidget()

        
        timerDisplay = QtGui.QLabel("0:00.00")
        
        self.setCentralWidget(timerDisplay)

        exitAction = QtGui.QAction(QtGui.QIcon(''), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar().showMessage("Ready")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')    
        self.show()        
            
            
    def loadSettings(self):
        '''
        If a settings file exists, then the settings are loaded from it. These override the default values.
        '''
        
        pass