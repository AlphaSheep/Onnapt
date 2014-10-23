'''
Created on 22 Oct 2014

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

from datetime import datetime

from Onnapt.utilities import getCurrentDateStamp, timeToStr


class SingleTime():
    '''
    A single solve with a time, scramble and datestamp.
    '''
    
    def __init__(self, scramble, solveTime, session = None, penalties = None, comment=''):
        self.dateStamp = getCurrentDateStamp()
        self.solveTime = solveTime
        self.session = session
        self.scramble = scramble
        self.penalties = penalties
        self.comment = comment        
       
        
    def getDBString(self):
        '''
        Gets a tab separated string for writing to the database
        '''
        if self.penalties:
            penaltyString = self.penalties
        else:
            penaltyString = ''
        if self.session:
            sessionIDstring = self.session.sessionID
        else:
            sessionIDstring = ''
        return self.dateStamp+'\t'+str(self.solveTime)+'\t'+penaltyString+'\t'+self.scramble+'\t'+sessionIDstring+'\t'+self.comment
    
    
    def getSolveTime(self, nDecimals):
        '''
        Returns the time in a convenient format
        '''
        return timeToStr(self.solveTime, nDecimals)
        
    
    
class Session():
    '''
    An object that keeps track of the history for a user
    '''

    def __init__(self):
        self.sessionID = getCurrentDateStamp()
        self.solve = []
    
    
    def addSolve(self, solve):
        self.solves.append(solve)
        
        
    
    


    
    
def test():
    s = Session()
    import time
    time.sleep(3.2)
    t = SingleTime("R U R' U R U2 R'", 83.2)
    s = SingleTime("R F' R' F", 16.124, s, 'DNF', 'No comment')
    print(t.getDBString())
    print(s.getDBString())


if __name__ == "__main__":
    test()