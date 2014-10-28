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
import time

from Onnapt.utilities import binaryListtoNumber
    
    

class StackMatTimer():
    '''
    A class for interacting with a StackMat timer
    '''

    def __init__(self):
        self.time = 0
        self.command = '?'
        self.state = 'Ready'
        
        self.listener = pyaudio.PyAudio()
        
        self.listeningfrequency = 24000
        self.targetbaud = 1200
        
        self.audioFormat = pyaudio.paUInt8
        
        self.frameSize = int(self.listeningfrequency/2)
        
        self.maxDataCapacity = 1200
        self.binaryData = []
        
        self.inputStream = self.listener.open(format = self.audioFormat, 
                                              channels = 1, 
                                              rate = self.listeningfrequency, 
                                              input = True,
                                              stream_callback = self.getCallback(),
                                              frames_per_buffer = self.frameSize)
        
        self.inputStream.start_stream()
        
        
        
    def stop(self):
        self.inputStream.stop_stream()
        self.inputStream.close()
        self.listener.terminate()
    
    
    def getCallback(self):
        def callback(in_data, frame_count, time_info, status):
            self.binaryData += self.analogToDigital(in_data)
            if len(self.binaryData) > self.maxDataCapacity:
                self.binaryData = self.binaryData[-self.maxDataCapacity:]
            self.updateState()
            return in_data, pyaudio.paContinue
        return callback

    
    def updateState(self):
        
        signals = self.getAllSignals()
       
        for signal in signals:
            
            stackmatTime, command = self.signalToTime(signal)
            if command != '?':
                self.command = command
            
            if command == 'I':
                self.state = "Ready"
                self.time = 0
            elif self.state == "Ready" and command == 'C':
                self.state = "Tapped"
            elif self.state == "Tapped" and command == 'C' and stackmatTime > self.time:
                self.time = stackmatTime                
            elif self.state in ["Ready", "Tapped"] and command == 'A' and stackmatTime < 0.1:
                self.state = "Armed"
            elif self.state == "Armed" and stackmatTime >= 0.1:
                self.state = "Running"
            elif self.state == "Running" and stackmatTime > self.time:
                self.time = stackmatTime
            elif command == 'S' or self.state == "Running" and stackmatTime == self.time and command == 'C':
                self.state = "Stopped"
            elif command == 'S':
                self.state = "Stopped"
                
    

    def analogToDigital(self, data):
        '''
        Takes an analog input signal and returns binary data as a list of 0 and 1.
        If the target baud is 1200 baud and the frequency is 24kHz, then the length of the binary data will be len(data)/20
        ''' 
        rawdata = []
        binaryData = []
        
        for item in data:
            rawdata.append(float(item))
        firstJump = 0
        
        jumpSize = max((max(rawdata) - min(rawdata))*0.6, 2.0)  # If the data is flat, then the jumpsize is 2 to prevent every step from being seen as a jump.
        midLevel = (max(rawdata) + min(rawdata))/2
        stepSize = self.listeningfrequency/self.targetbaud
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


    
    def getNextDataPos(self, data, blankDistance=16, dataEnd=False, lastData=False):
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
              
            
            

    def isolateNextSignal(self, binaryData):
        dataStart = self.getNextDataPos(binaryData)
        dataEnd = self.getNextDataPos(binaryData[dataStart:], dataEnd=True)+dataStart
        nextSignal = binaryData[dataStart:dataEnd]
        residual = binaryData[dataEnd:]
        return nextSignal, residual



    def getAllSignals(self):
        signals = []
        thisData, residual = self.isolateNextSignal(self.binaryData)
        while len(thisData) > 80:
            signals = [thisData] + signals 
            thisData, residual = self.isolateNextSignal(residual)
        return signals
    

    def signalToTime(self, signal):
    
        commandBin = signal[1:9]
        timeBin = [[],[],[],[],[]]
        timeBin[0] = signal[11:19]
        timeBin[1] = signal[21:29]
        timeBin[2] = signal[31:39]
        timeBin[3] = signal[41:49]
        timeBin[4] = signal[51:59]
        chckSumBin = signal[61:69]
        
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
        # print('Checksum - calculated:', checkSum, ', received: ', recievedCheckSum)
        # print('    '+command+' - Time = {:}:{:}{:}.{:}{:}'.format(num[0],num[1],num[2],num[3],num[4]))
        
            
        if recievedCheckSum == checkSum:
            # print('    '+command+' - Time = {:}:{:}{:}.{:}{:}'.format(num[0],num[1],num[2],num[3],num[4]))
            stackmatTime = num[0]*60 + num[1]*10 + num[2] + num[3]/10 + num[4]/100
            return stackmatTime, command
        
        return 0, command

            
        
def test():
    timer = StackMatTimer()
    
    while True:
        print("State: ",timer.state,'     Time: {:.2f}'.format(timer.time), timer.command)
        time.sleep(0.5)
            
        
if __name__ == "__main__":
    test()        
    