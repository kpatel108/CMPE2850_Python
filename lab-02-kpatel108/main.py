"""
CMPE2850 Lab02 - Snake
Author: Kalpan Patel
"""

import random
import sys
import time
import threading
import clr
dir(clr)

clr.AddReference('GDIDrawer')
clr.AddReference('System.Drawing')
from GDIDrawer import *
from System.Drawing import *


class Segment:
    # static dictionary mapping key input values to their respective direction
    keyMap = {
        37: (-1, 0),  # cursor-left     ->  (-1, 0)     (left) 37
        38: (0, -1),  # cursor-up       ->  (0, -1)     (up) 38
        39: (1, 0),  # cursor-right    ->  (1, 0)      (right) 39
        40: (0, 1),  # cursor-down     ->  (0, 1)      (down) 40
    }

    def __init__(self, segX, segY, segCol, segParent):
        self.segX = segX
        self.segY = segY
        self.segCol = segCol
        self.segParent = segParent

    # Equals() based on the x and y coordinates being the same.
    def __eq__(self, other):
        if other != None:
            return (self.segX == other.segX) & (self.segY == other.segY)

    def Show(self, canvas):

        if self.segParent != None:
            self.segParent.Show(canvas)
        canvas.AddCenteredEllipse(self.segX, self.segY, 1, 1, self.segCol)

    def Move(self, direction):
        mCoord = Segment.keyMap[int(direction)]

        if self.segParent == None:
            self.segX += mCoord[0]
            self.segY += mCoord[1]
        else:
            #         To make this work, each Segment must save the x and y of its parent BEFORE The recursive Move() call -
            #         thereby "remembering" where the parent WAS, then after the Move() call returns, this Segment moves into the
            #         "remembered" spot - it's parent has moved on. Clever Right ?
            #         Don't forget your recursion exit condition.. when do you stop ?
            parentX = self.segParent.segX
            parentY = self.segParent.segY
            self.segParent.Move(direction)
            self.segX = parentX
            self.segY = parentY


class Snake:
    # Class Snake
    #
    # A snake is made up of Segments. The tail segment will be held as a member. Move and Show are recursive and invoked
    # on the current tail( last ) Segment. Snakes will "grow". Different approaches abound. We will "grow" on a Move()
    # step, knowing our tail is in the last "safe" spot of our snake. Grow will add a new Segment in our last tail spot
    # after a Move.
    #
    # Members
    #
    #     an instance of Segment, representing the tail
    #     a grow bool representing if a growth Segment addition is required

    tailSeg = None
    grow = True

    #     CTOR accepts a starting x and y. Initialize the tail and grow members, add a new Segment as the tail/head of
    #     the snake using the x and y arguments, pick a random color and None for the parent ( Right ? ).

    def __init__(self, pX, pY):
        # RandColor.GetColor()
        self.tailSeg = Segment(pX, pY, RandColor.GetColor(), None)

    #     Show() accepts a CDrawer, invoke our Segment.Show() on the tail - it will recursively Show our entire snake.
    def Show(self, canvas):
        self.tailSeg.Show(canvas)

    #     Move() accepts a keycode direction.
    #         If grow is required, save the current tail position.
    #         Move() our tail - it will recurse and move our entire snake
    #         Now if grow is required, using your saved tail position, append a new Segment, be sure to specify the tail
    #         as the parent.
    #         Reset the grow flag, the growth has been handled.
    def Move(self, direction):

        if self.grow:
            tailPos = (self.tailSeg.segX, self.tailSeg.segY)

        self.tailSeg.Move(direction)

        if self.grow:
            newSeg = Segment(tailPos[0], tailPos[1], RandColor.GetColor(), self.tailSeg)
            self.tailSeg = newSeg
        self.grow = False

    #     GameOver() accepts a CDrawer( for boundary evaluation ), returns a bool indicating the end of the game.
    #         you must include at least these 2 conditions
    #             the snake has moved outside the CDrawer boundary
    #             the snake has hit "itself". Only the head moves right...
    def GameOver(self, canvas):

        if (self.Head()[1]>2) & (self.Head()[0] == self.tailSeg):
            #print(f'MaxLength {self.Head()[1]}')
            return True

        if ((self.Head()[0].segX > canvas.ScaledWidth) or (self.Head()[0].segX < 0)):
            #print(f'MaxLength {self.Head()[1]}')
            return True

        if ((self.Head()[0].segY > canvas.ScaledHeight) or (self.Head()[0].segY < 0)):
            #print(f'MaxLength {self.Head()[1]}')
            return True

        return False

    #     Head() helper function [optional] - returns the head Segment of the snake, and maybe the Snake length while you
    #     are at it.
    #
    def Head(self):
        count = 1
        snakeBit = self.tailSeg
        while snakeBit.segParent != None:
            count += 1
            snakeBit = snakeBit.segParent
        return (snakeBit, count)


def GetKeyCode(newCode=None,snake=None) -> 'tuple':
    myKeyCode = None
    with lock:
        global keyCode
        global maxLength
        global Speed

        if (newCode != None) & (newCode != keyCode):
            #updownleftright
            if(Segment.keyMap.__contains__(newCode)):
                keyCode = newCode
            elif (newCode == 109):
                Speed += 0.005

            elif (newCode == 107):
                if(Speed>0.05):
                    Speed -= 0.005
        myKeyCode = int(keyCode)
        if snake !=None:
            maxLength=snake.Head()[1]

    return (myKeyCode,maxLength)


# Locking for Snake
#
# There are a minimum of 3 global variables that will accessed across at least 3 threads.
#
#     keyCode - the variable holding the last key pressed by the user, supplied by the CDrawer and consumed within
#     the main processing thread.
#     running - the main running flag, indicating game/thread completion, accessed by __main__ and the game thread.
#     maxLength - the longest Segment count for the snake, accessed by __main__ and the game thread.
#
def GameThreadMethod(*args,**kwargs) -> 'tuple':

    global running
    global maxLength
    global Speed

    Speed = 0.05

    cScale = 20
    if 'scale' in kwargs:
        cScale = kwargs['scale']
    #
    # Initialize the current direction keyCode global to a random direction.
    keyCodes = [37, 38, 39, 40]

    global keyCode
    GetKeyCode(random.choice(keyCodes),None)

    #
    # Create and initialize the CDrawer, set the scale, continuous update and KeyboardCallback event to your handler
    # ( Ensure it properly locks the keyCode global when it assigns new values in event callback operations. )
    #

    canvas = CDrawer()
    canvas.ContinuousUpdate = False
    canvas.Scale = cScale

    canvas.KeyboardEvent += canvasKeyboardCallback

    gSnake = Snake(int(canvas.ScaledWidth / 2), int(canvas.ScaledHeight / 2))

    gTick = 0;

    appleEaten = True
    apple = None

    running=True
    while running:

        time.sleep(Speed)
        canvas.Clear()

        if appleEaten:
            aX = random.randint(0,canvas.ScaledWidth)
            aY = random.randint(0,canvas.ScaledHeight)
            apple = Segment(aX,aY,Color.Red,None)
            appleEaten = False
            print(f'Apple at {aX}-{aY}')

        apple.Show(canvas)


        # The thread will repeat indefinitely
        #     sleep for 15ms
        #     retrieve the current keyCode into a local
        currkeyCode = GetKeyCode()[0]
        if (currkeyCode != None) & (currkeyCode != keyCode):
            keyCode = currkeyCode

        #     Was it escape ? clear the running flag and break out of the loop
        if currkeyCode == 'escape':
            running = False

        #     Move the snake

        gSnake.Show(canvas)
        gSnake.Move(keyCode)
        canvas.Render()
        gTick += 1

        areWeDone = gSnake.GameOver(canvas)
        if(areWeDone):
            running=False;

        if (gTick % 20 == 0):
            gSnake.grow = True

        if(gSnake.Head()[0]==apple):
            gSnake.grow = True
            appleEaten=True

        maxLen = GetKeyCode(None, gSnake)[1]
        canvas.AddText(f'Current Score: {str(maxLen)}',10, Color.Red)
        canvas.AddText(f'+ / - Toggle speed [{round(Speed,3)}]',10,int(canvas.ScaledWidth/2)-15,int(canvas.ScaledHeight/2),30,10, Color.Yellow)

        #     Check for GameOver
        #     If Nms has elapsed, set your snake to grow
        #     Clear/Show/Render your snake
        #     update the current maxLength of the snake
        #
        # If you have broken out of the loop, Close() the CDrawer, clear your running flag and exit.



    canvas.Close()
    running = False;


# In .NET, the original definition for the CDrawer event callback is :
# private void _canvas_KeyboardEvent(bool bIsDown, System.Windows.Forms.Keys keyCode, CDrawer dr)
#
# So, matching the arguments, a matching callback function can be created
def canvasKeyboardCallback(IsDown, InkeyCode, can):
    # print(f"IsDown:{IsDown}, keyCode{InkeyCode}")
    if (Segment.keyMap.__contains__(int(InkeyCode)) or (int(InkeyCode)==27) or (int(InkeyCode)==107) or (int(InkeyCode)==109)):
        GetKeyCode(int(InkeyCode))


if __name__ == '__main__':
    # __main__
    #
    # Gets everything ready then spins until the game is over.
    #
    #     Define your globals, initializing your locks(s)
    global running

    # There are a minimum of 3 global variables that will accessed across at least 3 threads.
    #
    #     keyCode - the variable holding the last key pressed by the user, supplied by the CDrawer and consumed within
    #     the main processing thread.
    #     running - the main running flag, indicating game/thread completion, accessed by __main__ and the game thread.
    #     maxLength - the longest Segment count for the snake, accessed by __main__ and the game thread.

    keyCode = None
    running = True
    maxLength = 0
    lock = threading.Lock()

    #     Create and initialize your daemon thread with a keyword Scale arg, use 100 for debugging, then 20 for a real game.
    #     Start your thread
    gameThread = threading.Thread(target=GameThreadMethod,args=(1,), kwargs={'scale': 8}, daemon=True)
    gameThread.start()

    # effectively the same thing
    # input("Running Game\n")

    print('Game Running')
    while running:
        time.sleep(1)
    with lock:
        print(f'Current Score:{maxLength}')
