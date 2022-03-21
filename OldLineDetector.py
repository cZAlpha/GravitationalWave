from picar.utils import reset_mcu
from picar import picarx
import time

#IMPORT SECTION FOR DIFFERENT MODULES
import objectAvoidance



reset_mcu()
WALL_E = picarx.Picarx()

'''
Program to find and follow the boundary of the maze
by following the left side of the Maze until it finds
the end of the Maze
'''
#Change this value for a hard left turn
hardLeft = -27
#Change this value for a soft left turn
softLeft = -5
#Change this value for a hard right
hardRight = 30
#Change this value for a straight path
straight = 14
#Change this value for a soft right
softRight = straight + 3



def calibrate():
    #Change this value for a hard left turn
    hardLeft = -27
    #Change this value for a soft left turn
    softLeft = -5
    #Change this value for a hard right
    hardRight = 50
    #Change this value for a soft right
    softRight = 25
    #Change this value for a straight path
    straight = 14

    WALL_E.turn_wheels(straight)
    time.sleep(3)
    WALL_E.turn_wheels(hardLeft)
    time.sleep(1)
    WALL_E.turn_wheels(softLeft)
    time.sleep(1)
    WALL_E.turn_wheels(straight)
    time.sleep(1)
    WALL_E.turn_wheels(softRight)
    time.sleep(1)
    WALL_E.turn_wheels(hardRight)
    time.sleep(1)
    WALL_E.turn_wheels(straight)

def sense_line(cut_off=700):
    '''
    Read the line sensor values and use the cut_off value to return a list
    where each element is either 0 for black or 1 for white.
    '''

    #Initialize The list
    lineList = []
    readvalues = WALL_E.get_line_sensor_values()
    
    for value in readvalues:
        if value <= cut_off:
            #sees black
            lineList.append(1) 
        elif value >= cut_off:
            #sees not black
            lineList.append(0)
    #print(lineboi)
    return lineList

#Variable Init. Section
turnAngle = -5 #LEFT
turnStraight = 15 #STRAIGHT
turnSpeed = 5
forwardSpeed = 5

def getLineControlsLeft():
    '''
    Read line sensor and return a two tuple with the first element the speed
    and the second element the turn angle ie (speed, angle).
    '''
    readValues = sense_line()
    
    #Change this value for a hard left turn
    hardLeft = -27
    #Change this value for a soft left turn
    softLeft = -5
    #Change this value for a hard right
    hardRight = 30
    #Change this value for a straight path
    straight = 14
    #Change this value for a soft right
    softRight = straight + 3
    
    # Init. the two variables to be returned
    #Default Speed
    Speed = 1
    # Direction to go 
    Direction = 0
    # If it has hit the line
    FoundLine = False
    
    
    # straight
    if readValues == [1,0,0]:
        Direction = softRight
        FoundLine = True
        print("FOLLOWING LINE")
        
        
    # soft right
    elif readValues == [1,1,0]:
        Direction = softRight
        FoundLine = True 
    # hard right
    elif readValues == [1,1,1] or readValues == [1,0,1]:
        Direction = hardRight
        FoundLine = True
    # soft left
    elif readValues == [0,1,1] or readValues == [0,0,1]:
        Direction = hardLeft
        FoundLine = True
    # soft left
    elif readValues == [0,0,0]:
        Direction = softLeft
    # else
    else:
        print(readValues)
        print("Wall-E is having trouble finding the line!")
        Speed = 'None'
        Direction = 'None'
    
    return Speed, Direction, FoundLine, readValues

def findLineLeft(forwardSpeed = 5):
    '''
    This while loop serves to make the robot find the
    boundary line and then back up, then go parallel
    to it.
    '''
    
    #Change this value for a soft right
    softRight = 25
    #Change this value for a straight path
    straight = 14
    #Change this value for a soft left turn
    softLeft = -5
    
    forwardSpeed = forwardSpeed
    
    
    WALL_E.forward(forwardSpeed)
    WALL_E.turn_wheels(turnAngle)
    run = True
    while run == True:
        controls = getLineControlsLeft()
        print(controls)
        
        # If WALL_E finds the boundary
        if controls[2] == True:
            WALL_E.stop()
            WALL_E.turn_wheels(straight)
            run = False
        else:
            WALL_E.forward(forwardSpeed)
            
    # Notifies the console that the boundary has been found
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("WALL-E has found the boundary.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    time.sleep(1)
    
    WALL_E.backward(10)
    WALL_E.turn_wheels(-14)
    time.sleep(1)
    WALL_E.stop()
    WALL_E.turn_wheels(14)        
            

def isObjectDetected():
    objectAvoidance.start_avoidance() 


def followLineLeft():
    # Makes WALL_E find the boundary line
    findLineLeft()
    
    # Starts the process of following the boundary line and
    # stops WALL_E from moving if an object is detected
    run = True
    while run == True:        
        controlsInfo = getLineControlsLeft()
        speed = controlsInfo[0]
        directions = controlsInfo[1]
        sensorValues = controlsInfo[2]
        
        print("~~~~Instance~~~~~~~~~~")
        print("Speed: ", speed)
        print("Direction: ", directions)
        print("Sensor: ", sensorValues)
        print("~~~~~~~~~~~~~~~~~~~~~~")
        
        
            
        # Checks for errors in the getLineControlsLeft() function
        if (directions == 'None' and speed == 'None'):
            print("An error has occured. Please check the 'getLineControlsLeft()' function, as well as this one for errors in the code.")
            WALL_E.stop()
            run = False
        # Checks for objects in front of WALL_E
        
        elif (directions != 'None' and speed != 'None'):
            isObjectDetected()
            # INSERT FUNCTION THAT GOES AROUND OBJECT AND / OR CHECKS WHAT TYPE OF OBJECT IT IS
    
        # Controls the robot if other cases are false
        else:
            # Makes sure the robot turns for long enough to actuall stay in the boundaries
            if directions == hardRight or directions == softRight:
                WALL_E.stop()
                time.sleep(1)
                WALL_E.backward(speed)
                WALL_E.turn_wheels((directions) * -1)
                print("~~~~Backing Up~~~~~~~~")
                print("Speed: ", speed)
                print("Direction: ", directions)
                print("Sensor: ", sensorValues)
                print("~~~~~~~~~~~~~~~~~~~~~~")
                time.sleep(1)
            else:
                # Sets speed
                WALL_E.forward(speed)
                # Sets direction
                WALL_E.turn_wheels(directions)
            
    
def abc():
    objectAvoidance.start_avoidance()
    
    
    
    
