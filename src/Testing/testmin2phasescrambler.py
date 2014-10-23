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

from Slapt.utilities import createArray

class Scrambler333():
    '''
    Based on the scramble_333_edit.js used by qqtimer.net, which is in turn based on 
    Shuan Chen's min2phase solver that is used in the WCA official scrambler, TNoodle.
    '''
    
    def __init__(self):
        pass
    
    def clinit_CoordCube(self):
        self.UDSliceMove = createArray(495, 18);
        self.TwistMove = createArray(324, 18);
        self.FlipMove = createArray(336, 18);
        self.UDSliceConj = createArray(495, 8);
        self.UDSliceTwistPrun = createArray(160380);
        self.UDSliceFlipPrun = createArray(166320);
        self.TwistFlipPrun = createArray(870912);
        self.Mid3Move = createArray(1320, 18);
        self.Mid32MPerm = createArray(24);
        self.CParity = createArray(346);
        self.CPermMove = createArray(2768, 18);
        self.EPermMove = createArray(2768, 10);
        self.MPermMove = createArray(24, 10);
        self.MPermConj = createArray(24, 16);
        self.MCPermPrun = createArray(66432);
        self.MEPermPrun = createArray(66432);
        
    def initCParity(self):
        self.CParity = createArray(346)
        for i in range(2768):
            self.CParity[i >> 3] =  (self.CParity[i >> 3] | self.get8Parity((self.CPermS2R[i])) << (i&7))
        
    def initCPermMove(self):
        c = CubieCube_0()
        d = CubieCube_0()
        for i in range(2768):
            self.set8Perm(c.cp, (self.CPermS2R)[i])
            for j in range(18):
                self.CornMult(c, self.moveCube[j], d);
                self.CPermMove[i][j] = self.getCPermSym(d)
                
    def initEPermMove(self):
        c = CubieCube_0()
        d = CubieCube_0()
        for i in range(2768):
            self.set8Perm(c.ep, (self.EPermS2R)[i])
            for j in range(10):
                self.EdgeMult(c, self.moveCube[self.ud2std[j]], d);
                self.EPermMove[i][j] = self.getEPermSym(d)
            
    def initFlipMove(self):
        c = CubieCube_0()
        d = CubieCube_0()
        for i in range(336):
            self.setFlip(c, (Flip2SR)[i])
            for j in range(18):
                self.EdgeMult(c, self.moveCube[j], d)
                self.FlipMove[i][j] = self.getFlipSym(d)
                
    def initMCEPermPrun(self, callback):
        c = CubieCube_0()
        d = CubieCube_0()
        depth = 0
        done = 1
        SymState = createArray(2768)
        for i in range(2768):
            SymState[i] = 0
            self.set8Perm(c.ep, (self.EPermS2R)[i])
            for j in range(1, 16):
                self.EdgeMult(self.CubeSym[self.SymInv[j]], c, self.temp_0)
                self.EdgeMult(self.temp_0, self.CubeSym[j], d)
                if self.binarySearch(self.EPermS2R, self.get8Perm(d, ep)) != 65535:
                    SymState[i] = SymState[i] | (1 << j)
        for i in range(66432):
            self.MEPermPrun[i] = -1
            
        # Line 120 of original code was here...
        
        self.MEPermPrun[0] = 0
        while done<66432:
            inv = depth > 7
            if inv:
                select = -1
                check = depth
            else:
                select = depth
                check = -1
            depth += 1
            for i in range(66432):
                if self.MEPermPrun[i] == select:
                    mid = i % 24
                    edge = int(i/24)
                    for m_0 in range(10):
                        edgex = self.EPermMove[edge][m_0]
                        symx = edgex & 15
                        midx = self.MPermConj[self.MPermMove[mid][m_0]][symx]
                        edgex = edgex >> 4
                        idx = edgex * 24 + midx
                        if self.MEPermPrun[idx] == check:
                            done += 1
                            if inv:
                                self.MEPermPrun[i] = depth
                                break
                            else:
                                self.MEPermPrun[idx] = depth
                                sym = SymState[edgex]
                                if sym != 0:
                                    for j in range(16):
                                        sym = sym >> 1
                                        if (sym & 1) == 1:
                                            idxx = edgex * 24 + self.MPermConj[midx][j]
                                            if self.MEPermPrun[idxx] == -1:
                                                self.MEPermPrun[idxx] = depth
                                                done += 1
            callback("MEPermPrun: " + (int(done * 100 / 66432)) + "% (" + done + "/66432)")
        
        # Line 164 in original code was here...
                                              
        for i in range(66432):
            self.MCPermPrun[i] = -1
        self.MCPermPrun[0] = 0
        depth = 0
        done = 1
        while done < 66432:
            inv = depth > 7
            if inv:
                select = -1
                check = depth
            else:
                select = depth
                check = -1
            depth += 1
            for i in range(66432):
                if self.MCPermPrun[i] == select:
                    mid = i % 24
                    corn = int(i / 24)
                    for m_0 in range(10):
                        cornx = self.CPermMove[corn][self.ud2std[m_0]]
                        symx = cornx & 15
                        midx = self.MPermConj[self.MPermMove[mid][m_0]][symx]
                        cornx = cornx >> 4
                        idx = cornx * 24 + midx
                        if self.MCPermPrun[idx] == check:
                            done += 1
                            if inv:
                                self.MCPermPrun[i] = depth
                                break;
                            else:
                                self.MCPermPrun[idx] = depth
                                sym = SymState[cornx]
                                if sym != 0:
                                    for j in range(16):
                                        sym = sym >> 1
                                        if (sym & 1) == 1:
                                            idxx = cornx * 24 + self.MPermConj[midx][j**(self.e2c)[j]]
                                            if self.MCPermPrun[idxx] == -1:
                                                MCPermPrun[idxx] = depth
                                                done += 1
            callback("MCPermPrun: " + (int(done * 100 / 66432)) + "% (" + done + "/66432)")                                
            
    # line 215 of original code was here...
    
    def initMPermConj(self):
        c = CubieCube_0()
        d = CubieCube_0()
        for i in range(24):
            self.setMPerm(c, i)
            for j in range(16):
                self.EdgeConjugate(c, self.SymInv[j], d)
                self.MPermConj[i][j] = self.getMPerm(d)
                
    def initMPermMove(self):
        c = CubieCube_0()
        d = CubieCube_0()
        for i in range(24):
            self.setMPerm(c, i)
            for j in range(10):
                self.EdgeMult(c, self.moveCube[self.ud2std[j]], d);
                self.MPermMove[i][j] = self.getMPerm(d)           
                
    def initMid32MPerm(self):
        c = CubieCube_0()
        for i in range(24):
            self.setMPerm(c, i)
            self.Mid32MPerm[self.getMid3(c) % 24] = i
            
    def initMid3Move(self):
        c = CubieCube_0()
        d = CubieCube_0()
        for i in range(1320):
            self.setMid3(c, i)
            for jin range(18):
                self.EdgeMult(c, self.moveCube[j], d)
                self.Mid3Move[i][j] = self.getMid3(d)
            
    # Line 265 of original code was here...
            
            
            
            
            
            
            
            
            
            