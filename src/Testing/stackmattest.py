'''
Created on 27 Oct 2014

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


import pyaudio
import pylab
# import wave
# import sys

import time









def analogToDigital(data, frequency, targetbaud):
    '''
    Takes an analog input signal with a certain frequency and returns binary data as a list of 0 and 1.
    If targetbaud is 1200 baud and the frequency is 24kHz, then the length of the binary data will be len(data)/20
    ''' 

    rawdata = []
    binaryData = []
    
    for item in data:
        rawdata.append(float(item))
    firstJump = 0
    
    jumpSize = max((max(rawdata) - min(rawdata))*0.6, 2.0)  # If the data is flat, then the jumpsize is 2 to prevent every step from being seen as a jump.
    midLevel = (max(rawdata) + min(rawdata))/2
    stepSize = frequency/targetbaud
    # print('Jumpsize:', jumpSize, '    Midlevel:', midLevel, '    Stepsize:', stepSize)
    
    # Find the first jump to align the data
    
    for i in range(1, len(rawdata)):
        if abs(rawdata[i] - rawdata[i-1]) > jumpSize:            
            firstJump = i
            break

    if firstJump == 0:
        print ('Error: Timer seems to be switched off')
        for i in range(int(len(data)/stepSize)):
            binaryData.append(0)
        return binaryData
        
        
    i = firstJump + stepSize/2
    while i < len(rawdata):
        if rawdata[int(i)] < midLevel:
            binaryData.append(0)
        else:
            binaryData.append(1)
        i += stepSize
    
    return binaryData
    
    
    
def getNextDataPos(data, blankDistance=16, dataEnd=False, lastData=False):
    '''
    data is a list of 0 and 1. Returns the position at which the data starts, which is after blankDistance zeroes.
    If dataEnd is True, returns the position at which the data ends.
    If lastData is True, returns the last position
    '''
    blankStart = 0
    blanksEnd = 0
    blanks = 0
    for i in range(len(data)):
        if data[i] == 1:
            if blanks == 0:
                blankStart = i
            blanks += 1
            if blanks >= blankDistance:
                if dataEnd and not lastData:
                    return blankStart-1
        else:
            if blanks> blankDistance and not dataEnd:
                blanksEnd = i
                if not lastData:
                    return blanksEnd
            else:
                blanks = 0
    if lastData:
        if dataEnd:
            if blankStart >= blankDistance:
                return blankStart-1
        else:
            return blanksEnd        
    return 0
          
            
def binaryListtoNumber(bList):
    '''
    Takes a list of 1s and 0s, and returns the integer value of the binary number.
    Not that the binary numbers are in reverse (units on the left)
    '''
    
    value = 0
    power = 0
    for i in range(len(bList)):
        value += bList[i] * (2**power)
        power += 1
    return value
        
        
        
        
def printBinary(data):
    print('Data:')
    for i in range(len(data)):
        print("{:>4d}".format(i)[0], end="")
    print()
    for i in range(len(data)):
        print("{:>4d}".format(i)[1], end="")
    print()
    for i in range(len(data)):
        print("{:>4d}".format(i)[2], end="")
    print()
    for i in range(len(data)):
        print("{:>4d}".format(i)[3], end="")
    print()
    print()
    for d in data:
        print(d, end="")
    print()



def isolateNextSignal(data):
    dataStart = getNextDataPos(data)
    dataEnd = getNextDataPos(data[dataStart:], dataEnd=True)+dataStart
    nextSignal = data[dataStart:dataEnd]
    residual = data[dataEnd:]
    return nextSignal, residual



def getAllSignals(data):
    signals = []
    thisData, residual = isolateNextSignal(data)
    while len(thisData) > 80:
        signals = [thisData] + signals 
        thisData, residual = isolateNextSignal(residual)
    return signals
                
        


def signalToTime(binaryData):

    commandBin = binaryData[1:9]
    timeBin = [[],[],[],[],[]]
    timeBin[0] = binaryData[11:19]
    timeBin[1] = binaryData[21:29]
    timeBin[2] = binaryData[31:39]
    timeBin[3] = binaryData[41:49]
    timeBin[4] = binaryData[51:59]
    chckSumBin = binaryData[61:69]
    
    command = chr(binaryListtoNumber(commandBin))
    if command not in 'IA SLRC':
        command = '?'
    
    recievedCheckSum = binaryListtoNumber(chckSumBin)
    checkSum = 64
    
    num = []
    
    #print('Command signal', commandBin, binaryListtoNumber(commandBin))
    #print('Time data: ')
    for t in timeBin:
        num.append(binaryListtoNumber(t)-48)
        if num[-1] > 9:
            num[-1] = 0
        checkSum += num[-1]
    #print('Checksum - calculated:', checkSum, ', received: ', recievedCheckSum)
    
        
    if recievedCheckSum == checkSum:
        # print('    '+command+' - Time = {:}:{:}{:}.{:}{:}'.format(num[0],num[1],num[2],num[3],num[4]))
        stackmatTime = num[0]*60 + num[1]*10 + num[2] + num[3]/10 + num[4]/100
        return stackmatTime, command
    
    return 0, command
    
        
        
     

def main():
    FRAMESIZE = 12000
    FORMAT = pyaudio.paUInt8 # pyaudio.get_format_from_width(1)
    CHANNELS = 1
    RATE = 24000
    RECORD_SECONDS = 600
    
    FRAMESIZE = int(RATE/2)
    
    targetBaud = 1200     

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMESIZE)

    print("* recording")
    
    frames = []
    
    startTime = time.time()
    
    maxStackmatTime = 0
    lastcommand = 'I'

    for i in range(0, int(RATE / FRAMESIZE * RECORD_SECONDS)):
        data = stream.read(FRAMESIZE)
        # print('{:.2f} seconds of recording remaining'.format(RECORD_SECONDS - (time.time()-startTime)))
        frames.append(data)

        if i>1:
            data = frames[-2] + data # Include data from the previous frames in case a signal is spread over two frames
            
        binaryData = analogToDigital(data, RATE, targetBaud)    
        signals = getAllSignals(binaryData)
        for signal in signals:
            stackmatTime, command = signalToTime(signal)
            if command == 'I':
                maxStackmatTime = 0
            if stackmatTime > maxStackmatTime:
                maxStackmatTime = stackmatTime
            if command != '?' and command != lastcommand:
                print('                                                    command change:',command)
                lastcommand = command
        print('Listened for {:.1f} s,     Time displayed = {:.2f} s'.format((time.time()-startTime), maxStackmatTime))
        

    print("* done recording\n--------------\n\n")

    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    x = []
    y = []
    i = 0
    
    for data in frames:
        for item in data:
            x.append(i/RATE)
            y.append(float(item))
            i += 1
        binaryData = analogToDigital(data, RATE, 1200)    
        binaryToSignal(binaryData)
            
    
    #pylab.plot(x,y)
    #pylab.show()

if __name__ == '__main__':
    main()