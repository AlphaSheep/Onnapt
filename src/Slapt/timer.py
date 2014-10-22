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

import time

class PuzzleTimer():
    
    def __init__(self):
        self.currentTime = 0
        self.startTime = 0
        self.endTime = 0
        self.running = False
        
        
    def start(self):
        '''
        Starts the timer if it is not already started.
        '''
        if not self.running: 
            self.startTime = time.time()
            self.running = True
        
        
    def stop(self):
        '''
        Stops the timer if it is running
        '''
        if self.running:
            self.endTime = time.time()
            self.running = False
        
            
    def getTime(self):
        '''
        Returns the time in seconds since the timer was started
        '''
        if self.running:
            self.currentTime = time.time()
            return (self.currentTime - self.startTime)
        else:
            return (self.endTime - self.startTime)
        
        
    def isRunning(self):
        '''
        Returns True if the timer is currently running, False if not
        '''
        return self.running
    
    
def test(): 
    
    timer = PuzzleTimer()
    
    print("Testing timer")
    print("Press <Return> to start.")
    input()

    print("Running for about 10 seconds...\n")
    timer.start()
    for i in range(10):
        time.sleep(1)
        print("Running:", timer.isRunning(), " Time:", timer.getTime())
    timer.stop()

    for i in range(3):
        time.sleep(1)
        print("Running:", timer.isRunning(), " Time:", timer.getTime())

        
    timer.start()
    for i in range(5):
        time.sleep(1)
        print("Running:", timer.isRunning(), " Time:", timer.getTime())
    timer.stop()
    
    print("Running:", timer.isRunning(), " Time:", timer.getTime())
    
    
         
           
    
if __name__ == "__main__":
    test()
    
    
        
     
        