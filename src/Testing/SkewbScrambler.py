'''
Created on 23 Dec 2014

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

centercols = ['w','g','r','b','o','y'}

#                                                                                                                                                                     
#      c0                                                                                                                                  
#    x0  m0  x1  m1                                                                                                                    
#  c4  c1  c2  c3                                                                                                                   
#    m2  x2  m3 x3                                                                                                             
#      c5                                                                                                                               
#                                                                                                                                                                 
#                                                                                                                                                                 


class Skewb():
    
    def __init__(self):
        
        self.centersPerm = [0,1,2,3,4,5]
        self.fixedCornerPerm = [0,1,2,3]
        self.freeCornersPerm = [0,1,2,3]
        self.fixedCornerTwist = [0,0,0,0]
        self.freeCornersTwist = [0,0,0,0]
        
        
        
        


if __name__ == '__main__':
    pass





