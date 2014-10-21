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


class MainScreen(QtGui.QMainWindow):
    
    def __init__(self):

        super(MainScreen, self).__init__() # Call the constructor of this class's parent        
        self.prepare()
        
        self.initUI()
        
        # self.fpsTimer = QTimer()
        # self.fpsTimer.timeout.connect(self.updateDisplay)
        # self.fpsTimer.start(1000/targetFPS) # set targetFPS in constants.
        
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
        
        pass

        
    def initUI(self):
        '''
        Initialises the UI layout and widgets.
        '''
        
        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QtGui.QAction(QtGui.QIcon(''), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')    
        self.show()        
            