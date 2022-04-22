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
# Change this value for a hard left turn
hardleft = -27
# Change this value for a soft left turn
softleft = -5
# Change this value for a hard right
hardright = 50
# Change this value for a soft right
softright = 25
# Change this value for a straight path
straight = 14
# Change this value for the default speed
DEFAULT_SPEED = 10


def Main():
    functionList = [objectControls(), lineControls()]

    run = True
    while ( run ):
        for i in range(0, 2):
            # Sets the controls
            controls = functionList[i]

            # If there is no object, the PiCar uses Line Controls to drive
            if ( (controls == (None, None)) and ( i == 0 )):
                controls = functionList[1]
            # If there is an object, the PiCar avoids it
            elif ( i == 0 ):
                controls = functionList[0]
            # Catches weird cases / errors
            else:
                WALL_E.stop()
                print("AN ERROR HAS OCCURRED IN MAIN FOR LOOP")
                time.sleep(5)

            # Controlling robot portion
            WALL_E.forward( controls[0] )
            WALL_E.turn_wheels( controls[1] )



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
        return (DEFAULT_SPEED // 2, softleft)
    # straight
    elif readvalues == [1, 1, 0]:
        return (DEFAULT_SPEED, straight)
    # soft right
    elif readvalues == [1, 1, 1]:
        return (DEFAULT_SPEED, softright)
    # hard right
    elif readvalues == [0, 0, 1]:
        return (DEFAULT_SPEED // 2, hardright)
    # soft right
    elif readvalues == [0, 1, 1]:
        return (DEFAULT_SPEED, softright)
    # no line detected = soft left
    elif readvalues == [0, 0, 0]:
        return (DEFAULT_SPEED, softleft)

    # random stuff = go straight at default speed
    elif readvalues == [0, 1, 0] or readvalues == [1, 0, 1]:
        return (DEFAULT_SPEED, straight)


def isObject():
    thresholdValue = 35
    count = 0
    sensorSum = 0
    upperBound = 80
    returnValue = False

    isDone = False
    while ( not isDone ):
        # WHATEVER COMMAND IT IS TO TAKE THE LINE SENSOR VALUES
        sensorValue = WALL_E.???
        if ( sensorValue > 0 and  sensorValue < upperBound):
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
    # Globalizes the state variable
    global inObjectState

    # Variables
    turnAngle = 15
    straightAngle = 14
    turnSpeed = 10

    # Object detection
    objectDetected = isObject()


    if ( inObjectState == False ):
        # This case handles when the robot doesn't spot an object
        if ( objectDetected == False):
            return (None, None)

        # This case handles when the robot spots an object
        elif ( objectDetected == True):
            inObjectState = True
            return ( turnSpeed, turnAngle )

    elif ( inObjectState == True):
        # This case handles when the robot spots an object
        if ( objectDetected == True):
            return ( turnSpeed, turnAngle )

        # This case handles when the robot was already avoiding the object but needs to straighten out
        elif ( objectDetected == False ):
            WALL_E.turn_wheels(straightAngle)
            time.sleep(1)
            inObjectState = False
            return (None, None)
