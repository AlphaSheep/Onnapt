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
from Slapt.timer import PuzzleTimer
from Slapt.utilities import timeToStr


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
        
        self.ctrlkeytracker = [0, 0] # Keeps track of how many Ctrl keys are pressed now [0], and how many were pressed before the last change [1].
        self.puzzleTimer = PuzzleTimer()
        self.justStopped = False
        
        pass
        
    
    def updateDisplay(self):
        '''
        Updates the display
        '''
        
        
        currentTime = self.puzzleTimer.getTime()         
        self.timerDisplay.setText(timeToStr(currentTime, nDigits))

            
            
   
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
                # print("Left Ctrl pressed")
                self.ctrlkeytracker[1] = self.ctrlkeytracker[0]
                self.ctrlkeytracker[0] += 1
            else:
                # print("Right Ctrl pressed")
                self.ctrlkeytracker[1] = self.ctrlkeytracker[0]
                self.ctrlkeytracker[0] += 1
            self.handleCtrlSituation()
        
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            if self.puzzleTimer.isRunning():
                self.puzzleTimer.stop()
                self.justStopped = True

        print (int(event.key()))
        

        if debugModeEnabled:
            if event.key() == Qt.Key_A:
                self.puzzleTimer.startTime -= 60
            if event.key() == Qt.Key_S:
                self.puzzleTimer.startTime -= 600
            if event.key() == Qt.Key_D:
                self.puzzleTimer.startTime -= 3600
            
    
    def keyReleaseEvent(self, event):
        '''
        Handles key presses anywhere in the program.
        '''
        
        keyScanCode = event.nativeScanCode()
        if event.key() in [Qt.Key_Control, Qt.Key_Meta]: # Either a Ctrl key in Windows and Linux, or the Command key of a Mac
            if int(event.nativeScanCode()) < 80:
                # This is a messy work around, and I'm not sure it will always work.
                # print("Left Ctrl released")
                self.ctrlkeytracker[1] = self.ctrlkeytracker[0]
                self.ctrlkeytracker[0] -= 1
            else:
                # print("Right Ctrl released")
                self.ctrlkeytracker[1] = self.ctrlkeytracker[0]
                self.ctrlkeytracker[0] -= 1
            self.handleCtrlSituation()

        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            if self.justStopped:
                self.justStopped = False
                # Prevents the timer from restarting once a Ctrl key is released after stopping.
            elif not self.puzzleTimer.isRunning():
                self.puzzleTimer.start()
            
            
             
        
    def initUI(self):
        '''
        Initialises the UI layout and widgets.
        '''
        
        timerWindow = QtGui.QWidget()

        
        self.timerDisplay = StretchedLabel("0:00.00")
        
        self.setCentralWidget(self.timerDisplay)

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
    
    def handleCtrlSituation(self):
        '''
        Deals with starting and stopping the timer depending on the current Ctrl situation.
        Should only be called in keyPressEvent or keyReleaseEvent if the Ctrl key was involved in the event. 
        '''
        
        if self.justStopped:
            self.justStopped = False
            # Prevents the timer from restarting once a Ctrl key is released after stopping.
            return
        
        print("Running:", self.puzzleTimer.isRunning(), "... Ctrl keys pressed:", self.ctrlkeytracker)
        if self.puzzleTimer.isRunning():
            if self.ctrlkeytracker[0] == 2:
                # If the timer was running, and both Ctrl keys are pressed.
                self.puzzleTimer.stop()
                self.justStopped = True
        else:
            if self.ctrlkeytracker == [1,2]:
                # If the timer was not running, and one Ctrl key is released after both having been pressed.                
                self.puzzleTimer.start()
                    
        
        
        
class StretchedLabel(QtGui.QLabel):
    '''
    A label with centred text that automatically resizes the font to fill the available space 
    '''
    
    def __init__(self, *args, **kwargs):
        QtGui.QLabel.__init__(self, *args, **kwargs)
        self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, evt):
        font = self.font()
        newSize = min(self.height() * 0.7, self.width() / 8)
        font.setPixelSize(newSize)
        self.setFont(font)    
    
    
    