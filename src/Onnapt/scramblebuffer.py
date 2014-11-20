'''
Created on 20 Nov 2014

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


import multiprocessing
from queue import Full, Empty

from PyQt4.QtCore import QTimer

from Onnapt.constants import *


class ScrambleBuffer():
    '''
    Uses threading to generate extra scrambles in the background. 
    '''
    
    def __init__ (self, scrambler):
        self.buffer = multiprocessing.Queue(scrambleBufferSize)
        self.scrambler = scrambler
        
        self.fails = 0
        
        self.fpsTimer = QTimer()
        self.fpsTimer.timeout.connect(self.updateQueue)
        self.fpsTimer.start(scrambleUpdateInterval)  # set targetFPS in constants.
        
        self.updateQueue()
        
        
    def getNextScramble(self):
        '''
        Retrieves a scramble from the queue.
        '''
        newScramble = self.buffer.get()
        self.updateQueue()
        return newScramble
        
    
    def updateQueue(self):
        '''
        Starts a new process to add a new scramble to the queue. This function should be called 
        intermittently, preferably on a timer. 
        '''
#        print('Creating seperate process for scramble generator...')
        process = multiprocessing.Process(target=self.addScramble)
#        print('Process ready, starting...')
        process.start()
#        print('Process running...')
        
        
    def addScramble(self):
        '''
        Attempts to add a new scramble to the buffer.
        '''        
        try:
            if not self.buffer.full() or self.fails > scrambleForceUpdateAttempts:
                newScramble = self.scrambler.nextScramble()
                print(newScramble)
                self.buffer.put(self.scrambler.nextScramble())
                self.fails = 0
            else:
#                print('Scramble buffer is full')
                self.fails += 1
        except Full:
 #           print('Error: Scramble buffer was unexpectedly full')
            self.fails += 1
             
            
