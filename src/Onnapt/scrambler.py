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

import random

from Onnapt.utilities import listWithout


class CubeScramblerByRandomTurns():
    '''
    Generates an object which returns random scrambles for a standard cube puzzle
    Scrambles consist of a number of randomly generated moves
    '''
    
    def __init__(self, size=3):
        self.size = size
        self.getAllowedTurns()
        self.setScrambleLength(0)
        self.scrambles = []
        
        
    def setScrambleLength(self, scrambleLength):
        '''
        Set the length of the generated scrambles. Set to 0 to use the default length for the puzzle size. 
        '''
        if scrambleLength:
            self.useDefaultLength = False
            self.scrambleLength = scrambleLength
        else:
            self.useDefaultLength = True
            self.scrambleLength = self.getScrambleLength()
        
        
    def getAllowedTurns(self):
        '''
        Builds a list of allowed turns based on the puzzle size
        '''        
        postfixes = ["", "'", "2"]        
        allowedTurns = ["U","F","R"]
        allowedWideTurns = []
        if self.size > 2:
            allowedTurns += ["D","L","B"]            
        if self.size > 3:
            allowedWideTurns += ["Uw","Fw","Rw","Dw","Lw","Bw"]
        prefixes = [""]
        maxprefix = int(self.size/2)
        if maxprefix > 2:
            for i in range(3, maxprefix+1):
                prefixes.append(str(i))
        
        for t in allowedWideTurns:
            for p in prefixes:
                allowedTurns.append(p+t)
        
        allTurns = [] 
        for t in allowedTurns:
            for p in postfixes:
                allTurns.append(t+p)
                
        return allTurns
        
        
    def getScrambleLength(self):
        '''
        If a scramble length has been set, then returns that. If not, then it returns a length based on the puzzle size
        '''
        if not self.useDefaultLength:
            return self.scrambleLength
        elif self.size < 4:
            return 25
        elif self.size < 9:
            return (self.size-2)*20
        else:
            return 120
        
        
    def nextScramble(self):
        length = 0
        scramble = ''
        lastTurn = ''
        allowedTurns = self.getAllowedTurns()
        while length < self.scrambleLength:            
            lastBase = lastTurn.rstrip("'2")
            skip = [lastBase, lastBase+"'", lastBase+"2"]
            lastTurn = random.choice(listWithout(allowedTurns, skip))
            scramble += lastTurn+' '
            length += 1
        self.scrambles.append(scramble[:-1])
        return self.scrambles[-1]
                    

def test():
    for size in range(2,14):
        print(size,'x',size,'x',size,'.   ',CubeScramblerByRandomTurns(size).nextScramble(), sep='')


if __name__ == "__main__":
    test()
