'''
Created on 23 Oct 2014

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

def loadScrambles(fileName):
    with open(fileName) as scrambleFile:
        scrambles = scrambleFile.readlines()
        for i in range(len(scrambles)):
            scrambles[i] = scrambles[i].strip()
    return scrambles
        
    
def testWCA():
    # Note that 2x2 - 4x4 are random state, 5x5 - 7x7 are n random turns
    
    puzzles = ['2x2x2', '3x3x3', '4x4x4', '5x5x5', '6x6x6', '7x7x7']
    for j in range(len(puzzles)):
        print(puzzles[j])
        scrambles = loadScrambles("./Sample scrambles/"+puzzles[j]+" Cube Round 1.txt")
        for i in range(len(scrambles)):
            print('    ',i,'. Length: ', len(scrambles[i].split(' ')), '    Scramble: ',scrambles[i], sep='')
        print('\n')


def main():
    #testWCA()
    
    scrambles = loadScrambles("./Sample scrambles/3x3test2.txt")
    for i in range(len(scrambles)):
        print('    ',i,'. Length: ', len(scrambles[i].split(' ')), '    Scramble: ',scrambles[i], sep='')
    


if __name__ == '__main__':
    main()