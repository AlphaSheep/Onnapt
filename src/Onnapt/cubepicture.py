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

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyQt4 import QtCore, QtGui


class CubePicture(FigureCanvas):
   
    def __init__(self, parent=None, nLayers=3, cubeColours='wgrboy'):
        
        self.nLayers = nLayers
        self.cubeColours = cubeColours
        
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111, projection='3d')
        self.figure.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0)
        
        self.axes.patch.set_visible(True)
        
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        colour = self.palette().color(QtGui.QPalette.Window).getRgbF()
        self.figure.set_facecolor(colour)
        self.axes.set_axis_bgcolor(colour)
        
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.updateGeometry()
        
        self.cube = Cube(self.axes, self.nLayers, self.cubeColours)
        
        
        
    def updateScramble(self, scramble):
        
        self.axes.cla()
        self.axes.view_init()
        self.axes.mouse_init()
        
        self.cube = Cube(self.axes, self.nLayers, self.cubeColours)
        self.cube.applyAlg(scramble)
        self.cube.display()
             
        self.draw()
        
        
        
    def draw(self):
        '''
        Overrides the default draw method to make sure axes and tick lables, etc are cleared first.
        '''
        
        self.axes.set_axis_off()
        self.axes.set_xticks([],[])
        self.axes.set_yticks([],[])
        self.axes.set_zticks([],[])

        for axis in self.axes.w_xaxis, self.axes.w_yaxis, self.axes.w_zaxis:
            axis.pane.set_visible(False)
            axis.line.set_visible(False)
            
        FigureCanvas.draw(self)
        
        

class Point():
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
        
    def rotate(self, face, nLayers):
        centre = Point((nLayers-1)/2.0, (nLayers-1)/2.0, (nLayers-1)/2.0)
        offsetPoint = self - centre
        rot = getRotationMatrix(face) 
        newPoint = (offsetPoint*rot)
        return (newPoint + centre).fixToInt()

        
    def fixToInt(self):
        self.x = float(int(self.x))
        self.y = float(int(self.y))
        self.z = float(int(self.z))
        return self
    
   # def __list__(self):
   #     return [self.x, self.y, self.z]    
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z 
    
    def __len__(self):
        return 3
    
    def __add__(self, other):
        if type(other)== list:
            return Point(self.x+other[0], self.y+other[1], self.z+other[2])
        else:
            return Point(self.x+other.x, self.y+other.y, self.z+other.z)
    
    
    def __sub__(self, other):
        if type(other)== list:
            return Point(self.x-other[0], self.y-other[1], self.z-other[2])
        else:
            return Point(self.x-other.x, self.y-other.y, self.z-other.z)
    
    
    def __mul__(self, other):
        x = other[0][0]*self.x + other[0][1]*self.y + other[0][2]*self.z
        y = other[1][0]*self.x + other[1][1]*self.y + other[1][2]*self.z
        z = other[2][0]*self.x + other[2][1]*self.y + other[2][2]*self.z
        return Point(x, y, z)
        
    
    def __repr__(self):
        return 'Point: '+str(self.x)+', '+str(self.y)+', '+str(self.z)
        
        
class Face():
    
    def __init__(self, vertices):
        self.vertices = vertices
        
        

class Cubie():
    
    def __init__(self, home, position, orientation, parent):
        
        self.parent = parent
        self.home = home
        self.position = position
        self.orientation = orientation
        
        self.colours = self.getColours()
        

    def renewFaces(self):
        
        offset = self.position
        
        startPos = 0.05
        endPos = 0.95
        
        self.faces = []
        self.faces.append(Face([Point(startPos, startPos, endPos)+offset, Point(startPos, endPos, endPos)+offset, Point(endPos, endPos, endPos)+offset, Point(endPos, startPos, endPos)+offset])) # top
        self.faces.append(Face([Point(startPos, startPos, startPos)+offset, Point(startPos, startPos, endPos)+offset, Point(endPos, startPos, endPos)+offset, Point(endPos, startPos, startPos)+offset])) # front
        self.faces.append(Face([Point(endPos, startPos, startPos)+offset, Point(endPos, startPos, endPos)+offset, Point(endPos, endPos, endPos)+offset, Point(endPos, endPos, startPos)+offset])) # right
        self.faces.append(Face([Point(startPos, endPos, startPos)+offset, Point(startPos, endPos, endPos)+offset, Point(endPos, endPos, endPos)+offset, Point(endPos, endPos, startPos)+offset])) # back
        self.faces.append(Face([Point(startPos, startPos, startPos)+offset, Point(startPos, startPos, endPos)+offset, Point(startPos, endPos, endPos)+offset, Point(startPos, endPos, startPos)+offset])) # left
        self.faces.append(Face([Point(startPos, startPos, startPos)+offset, Point(startPos, endPos, startPos)+offset, Point(endPos, endPos, startPos)+offset, Point(endPos, startPos, startPos)+offset])) # bottom
    
    
    def getVertices(self):
        
        self.renewFaces()
        vertices = []
        for face in self.faces:
            vertices.append(list(face.vertices))
        return vertices

    
    def getColours(self):
        
        baseColours = self.parent.baseColour[:]
        targetColours = self.parent.colours[:]
        
        colours = baseColours[:]
        
        pos = self.home
        n = self.parent.nLayers-1
        
        if pos.z==n: colours[0] = targetColours[0] # top
        if pos.y==0: colours[1] = targetColours[1]  # front
        if pos.x==n: colours[2] = targetColours[2] # right
        if pos.y==n: colours[3] = targetColours[3] # back
        if pos.x==0: colours[4] = targetColours[4] # left
        if pos.z==0: colours[5] = targetColours[5] # bottom
        
        return colours
        

    def turn(self, face):

        self.position = self.position.rotate(face, self.parent.nLayers)
        self.colours = rotateColours(self.colours, face)

        
        
            
    def inLayer(self, face, layers):
        pos = self.position
        if face == 0: # top
            if pos.z >= self.parent.nLayers-layers:
                return True
            else:
                return False
        if face == 1: # front
            if pos.y < layers:
                return True
            else:
                return False
        if face == 2: # right
            if pos.x >= self.parent.nLayers-layers:
                return True
            else:
                return False
        if face == 3: # back
            if pos.y >= self.parent.nLayers-layers:
                return True
            else:
                return False
        if face == 4: # left
            if pos.x < layers:
                return True
            else:
                return False
        if face == 5: # bottom
            if pos.z < layers:
                return True
            else:
                return False
    
    
    def display(self, axis):
        
        verts = self.getVertices()
        
        cubie = Poly3DCollection(verts, linewidth=2)
        cubie.set_facecolors(self.colours)
        cubie.set_edgecolor('k')
        
        axis.add_collection3d(cubie)
        
    

class EdgeCubie(Cubie):
    pass
        
class CornerCubie(Cubie):
    pass

class CentreCubie(Cubie):    
    pass

        
class Cube():
    '''
    General class for cubes with 3 or more layers
    '''
    
    def __init__(self, displayAxes, nLayers=3, colours='wgrboy'):
        
        self.axes = displayAxes
        
        self.nLayers = nLayers
        self.colours = translateColours(colours)
        
        self.baseColour = translateColours('kkkkkk')
        
        self.cubies = {}
        
        for x in range(nLayers):
            for y in range(nLayers):
                for z in range(nLayers):
                    
                    cubiePos = 0
                    pos = Point(x,y,z)

                    if x==0: cubiePos += 1 
                    elif x==nLayers-1: cubiePos += 1
                    if y==0: cubiePos += 1
                    elif y==nLayers-1: cubiePos += 1
                    if z==0: cubiePos += 1
                    elif z==nLayers-1: cubiePos += 1
                        
                    if cubiePos == 3:
                        self.cubies[pos] = CornerCubie(Point(x,y,z), Point(x,y,z), [0,0,0], self)
                    elif cubiePos == 2:
                        self.cubies[pos] = EdgeCubie(Point(x,y,z), Point(x,y,z), [0,0,0], self)
                    elif cubiePos == 1:
                        self.cubies[pos] = CentreCubie(Point(x,y,z), Point(x,y,z), [0,0,0], self)
                        
                        
    def turn(self, *args):
        '''
        Turns a number of layers about a certain face in a given direction. Face is a number from 0 to 5.
        direction of 1 means a 90deg clockwise turn, 2 means 180deg turn, and -1 means 
        '''
        
        if len(args) == 3:            
            face, direction, layers = args
        elif len(args) == 1:
            face, direction, layers = translateTurn(args[0])
        
        if layers == 0:
            layers = self.nLayers
            
        while direction > 3: direction -= 4
        while direction < 0: direction += 4
            
        if direction == 1:
            self.singleTurn(face, layers)
        elif direction ==2:
            self.singleTurn(face, layers)
            self.singleTurn(face, layers)
        elif direction == 3:
            self.singleTurn(face, layers)
            self.singleTurn(face, layers)
            self.singleTurn(face, layers)
            
            
    def singleTurn(self, face, layers):
        
        for cubiePos in self.cubies.keys():
            if self.cubies[cubiePos].inLayer(face, layers):
                self.cubies[cubiePos].turn(face)
        
    
        
    def applyAlg(self, alg):
        
        moves = alg.strip().split(' ')
        for move in moves:
            self.turn(move.strip())
                      
                        
    def display(self):
        
        for cubiePos in self.cubies.keys():
            self.cubies[cubiePos].display(self.axes)
        
        self.axes.set_aspect("equal")
        self.axes.set_xlim([0,self.nLayers])
        self.axes.set_ylim([0,self.nLayers])
        self.axes.set_zlim([0,self.nLayers])
        #self.axes.set_axis_off()

        
        
        
     
     
def getRotationMatrix(face):
    if face == 0: return [[0, 1, 0],[-1, 0, 0],[0, 0, 1]] # top
    if face == 1: return [[0, 0, 1],[0, 1, 0],[-1, 0, 0]] # front
    if face == 2: return [[1, 0, 0],[0, 0, 1],[0, -1, 0]] # right
    if face == 3: return [[0, 0, -1],[0, 1, 0],[1, 0, 0]] # back
    if face == 4: return [[1, 0, 0],[0, 0, -1],[0, 1, 0]] # left
    if face == 5: return [[0, -1, 0],[1, 0, 0],[0, 0, 1]] # bottom
            

def getOrientationMap(face):
    if face == 0: return [0, 2, 3, 4, 1, 5] # top
    if face == 1: return [4, 1, 0, 3, 5, 2] # front
    if face == 2: return [1, 5, 2, 0, 4, 3] # right
    if face == 3: return [2, 1, 5, 3, 0, 4] # back
    if face == 4: return [3, 0, 2, 5, 4, 1] # left
    if face == 5: return [0, 4, 1, 2, 3, 5] # bottom


def rotateColours(colours, face):
    omap = getOrientationMap(face)
    newColours = colours[:]
    for i in range(len(colours)):
        newColours[i] = colours[omap[i]]
    return newColours 
    
                    
def translateColours(colours):
        
    colourList = []
    for colour in colours:
        if colour == 'o':
            colourList.append('#ff8000')
        else:
            colourList.append(colour)
    return colourList


def translateTurn(turn):
    
    turnDict = {'U':0, 'F':1, 'R':2, 'B':3, 'L':4, 'D':5}
    rotDict = {'x':0, 'y':1, 'z':2}

    wideTurnTranslator = {'u':'Uw', 'f':'Fw', 'r':'Rw', 'b':'Bw', 'l':'Lw', 'd':'Dw'}
    
    for w in wideTurnTranslator.keys():
        turn = turn.replace(w, wideTurnTranslator[w])
    
    if turn[-1] in ("'", '2'):
        postfix = turn[-1]
        turn = turn[:-1]
    else: 
        postfix = ''

    if turn[-1] == 'w':        
        prefix = turn[:-2]
        baseTurn = turn[-2]
        layers = 2
    else:
        prefix = turn[:-1]
        baseTurn = turn[-1]
        layers = 1
        
    if not baseTurn in (list(turnDict.keys()) + list(rotDict.keys())):
        raise Exception('Unrecognised turn', turn)    

    face = turnDict[baseTurn]
    
    if len(prefix)>0:
        layers = int(prefix)
    
    if postfix == "'":
        direction = 3
    elif postfix == '2':
        direction = 2
    else: 
        direction = 1
    
    return face, direction, layers


