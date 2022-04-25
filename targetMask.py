# IMPORT SECTION
# <INSERT IMPORTS>
from picar.utils import reset_mcu
from picar import picarx
import time

reset_mcu()
WALL_E = picarx.Picarx()



# GLOBAL STATE VARIABLES
inObjectState = False
currentLineState = "NO_LINE"

# VARIABLE SECTION
#change this for straight path
straight=0
# Change this value for a hard left turn
hardleft = straight-20
# Change this value for a soft left turn
softleft = straight-15
# Change this value for a hard right
hardright = straight+20
# Change this value for a soft right
softright = straight+15
# Change this value for the default speed
DEFAULT_SPEED = 3


def Main():
    print("Main Initiated...")
    print("")
    
    run = True
    while ( run ):
        print("Before Object Controls")
        print("")
        objControls=objectControls()
        print("Before Line Controls")
        print("")
        lnControls=lineControls()
        print("**********************")
        
        # If there is no object, the PiCar uses Line Controls to drive
        if (objControls == (None, None) ):
            # Controlling robot portion
            WALL_E.forward(lnControls[0] )
            WALL_E.turn_wheels(lnControls[1] )
            print("In Line Controls")
            
        # If there is an object, the PiCar avoids it
        elif(not objControls==(None,None)):
            WALL_E.forward(objControls[0] )
            WALL_E.turn_wheels(objControls[1] )
            print("In Object Controls")
            
        # An error case, Line function should never return (None, None)
        elif ( lnControls == (None, None) ):
            print("Controls equaled None while not in Object function for some reason. Fix it.")
            run = False
            


def sense_line(cut_off=700):
    '''
    Read the line sensor values and use the cut_off value to return a list
    where each element is either 0 for black or 1 for white.
    '''

    # Initialize The list
    lineList = []
    readvalues = WALL_E.get_line_sensor_values()

    for value in readvalues:
        if value <= cut_off:
            # sees black
            lineList.append(1)
        elif value >= cut_off:
            # sees not black
            lineList.append(0)
    return lineList


def lineControls():
    '''
    Read line sensor and return a two tuple with the first element the speed
    and the second element the turn angle ie (speed, angle).
    '''
    readvalues = sense_line()

    # soft left
    if readvalues == [1, 0, 0]:
        print("Soft Left")
        return (DEFAULT_SPEED // 2, softleft)
    # straight
    elif readvalues == [1, 1, 0]:
        print("Straight")
        return (DEFAULT_SPEED, straight)
    # soft right
    elif readvalues == [1, 1, 1]:
        print("Soft Right")
        return (DEFAULT_SPEED, softright)
    # hard right
    elif readvalues == [0, 0, 1]:
        print("Hard Right")
        return (DEFAULT_SPEED // 2, hardright)
    # soft right
    elif readvalues == [0, 1, 1]:
        print("Soft Right")
        return (DEFAULT_SPEED, hardright)
    # no line detected = soft left
    elif readvalues == [0, 0, 0]:
        print("Soft Left")
        return (DEFAULT_SPEED, softleft)

    # random stuff = go straight at default speed
    elif readvalues == [0, 1, 0] or readvalues == [1, 0, 1]:
        print("Random Stuff")
        return (DEFAULT_SPEED, straight)


def isObject():
    print("*************")
    print("In isObject()")
    print("*************")
    thresholdValue = 35
    count = 0
    sensorSum = 0
    upperBound = 80
    returnValue = False

    isDone = False
    while ( not isDone ):
        # WHATEVER COMMAND IT IS TO TAKE THE OBJECT SENSOR VALUES
        sensorValue = WALL_E.get_distance()
        if ( (sensorValue > 0 and sensorValue < upperBound) or sensorValue == -2):
            sensorSum += sensorValue
            count += 1
        isDone = count > 6

    # Finds the average
    sensorAverage = sensorSum / count

    if ( sensorAverage < thresholdValue ):
        returnValue = True
    else:
        returnValue = False
    return returnValue


def objectControls():
    print("*****************")
    print("In objectControls")
    print("*****************")
    
    # Globalizes the state variable
    global inObjectState

    # Variables
    turnAngle = straight + 6
    straightAngle = straight
    turnSpeed = 3

    # Object detection
    objectDetected = isObject()


    if ( inObjectState == False ):
        # This case handles when the robot doesn't spot an object
        if ( objectDetected == False):
            print("inObjectState == False")
            print("objectDetected == False")
            return (None, None)

        # This case handles when the robot spots an object
        elif ( objectDetected == True):
            print("inObjectState == False")
            print("objectDetected == True")
            inObjectState = True
            return ( turnSpeed, turnAngle )

    elif ( inObjectState == True):
        # This case handles when the robot spots an object
        if ( objectDetected == True):
            print("inObjectState == True")
            print("objectDetected == True")
            return ( turnSpeed, turnAngle )

        # This case handles when the robot was already avoiding the object but needs to straighten out
        elif ( objectDetected == False ):
            print("inObjectState == True")
            print("objectDetected == False")
            WALL_E.turn_wheels(straightAngle)
            #time.sleep(1)
            inObjectState = False
            return (None, None)
