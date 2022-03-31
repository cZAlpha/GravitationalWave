# THIS IS THE NEW OBJECT AVOIDANCE PROGRAM / FILE

# TO - DO:
# 1. Fully implement (from scratch or other means) the avoidance(islineDetectedOutput) function, which will takes
#       the output of the isLineDetected() function as a perameter and then controls the robot's driving accordingly

# Sets up the imports needed
from picar.utils import reset_mcu
from picar import picarx
import time

# Sets up the PiCar
reset_mcu()
WALL_E = picarx.Picarx()

def getDistance():
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THIS IS A SUBFUNCTION OF 'isObjectDetected'
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This function serves to return the distance of any detected
    object.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''

    # Gathers data from the distance sensor
    reading1 = WALL_E.get_distance()
    reading2 = WALL_E.get_distance()
    reading3 = WALL_E.get_distance()
    reading4 = WALL_E.get_distance()
    reading5 = WALL_E.get_distance()
    reading6 = WALL_E.get_distance()

    # Checks if there were any detector errors (usually will be a reading less than 0)
    if (reading1 > 0 and reading2 > 0 and reading3 > 0 and reading4 > 0 and reading5 > 0 and reading6 > 0 ):
        # Gets the average of the readings and returns it
        average = (reading1 + reading2 + reading3 + reading4 + reading5 + reading6) / 6
        return average
    # If there were any errors, reruns the function
    else:
        getDistance()


def isObjectDetected():
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THIS IS THE PARENT FUNCTION OF 'getDistance'
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This function will return a Boolean value based on whether or not -
    there is an object detected within the distance specified within  -
    the variable 'distanceThreshold
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''

    # The distance, in centimeters, at which the detector will return true if there is an object
    distanceThreshold = 35
    # The variable that holds whether or not an object has been detected
    objectBool = False
    # The variable that holds the average distance of the object detected
    distanceOfObject = getDistance()

    # Checks if the object sensed is less than the distance variable value
    if ( distanceOfObject < distanceThreshold):
        objectBool = True
    return objectBool


def isLineDetected():
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This function will return a Boolean value based on whether or not -
    there is a line detected underneath the PiCar
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''

    # This variable holds the list for the line sensor readings
    lineList = []
    # This variable holds the values of the sense readings (not in list form)
    readValues = WALL_E.get_line_sensor_values()
    # This variable holds the Boolean value that tells whether or not the line has been sensed
    lineDetectedValue = 0
    # This variable acts as the threshold at which the sensor will consider a line black
    cut_off = 700


    # This for loop serves to fill in the 'lineList' list
    # with the sensor value readings from the variable
    # 'readValues'
    for value in readValues:
        if value <= cut_off:
            # sees black
            lineList.append(1)
        elif value >= cut_off:
            # sees not black
            lineList.append(0)
    
    lineList = [0,1,1]
    
    print("Line List:", lineList)
    print("Read Values:", readValues)

    # No Line Detected
    if (lineList == [0,0,0]):
        lineDetectedValue = 0
    # Left Line Detected
    elif (lineList == [1,0,0]) or (lineList == [1,1,0]):
        lineDetectedValue = 1
    # Right Line Detected
    elif (lineList == [0,1,1]) or (lineList == [0,0,1]):
        lineDetectedValue = 2
    # Mid / Weird case
    elif (lineList == [1,1,1]) or (lineList == [1,0,1]) or (lineList == [0,1,0]):
        lineDetectedValue = 3
    # else
    else:
        print("~~~~~~~~~~~~Sensor Error~~~~~~~~~~~~~~")
        print("Sensor Values: ", readValues)
        print("Sensor List: ", lineList)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("This message has been generated")
        print("because there was either:")
        print("  - A case not covered in the if")
        print("    statments of the isLineDetected()")
        print("    function in 'newObjectAvoidance' ")
        print("  - Some of the code did not work well")
        print("  - There was a catastrophic error in")
        print("    the sensors at some point")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    return lineDetectedValue
