import pigpio
from enum import Enum

class Motor:
    def __init__(self, io_object, PIN_ID_1, PIN_ID_2, MAX_DELTA = 100):
        # Create the shared io.pi() io object once 
        # Create two separate motor objects with its each pin numbers 
        # pinLegA : gpio pin number for Leg A (forward lead)
        # pinLegB : gpio pin number for Leg B (backwards lead)
        # Create the MAX_DELTA variable which shows how low the duty cycle can go
        #   This is to avoid the dutycycle = 0 -> motor break condition

        self.PIN_ID_1 = PIN_ID_1
        self.PIN_ID_2 = PIN_ID_2

        self.MAX_DELTA = MAX_DELTA

        self.io = io_object        
        
        self.MAX_PWM = 255

        self.init_PWM(1000)
        self.io.set_PWM_dutycycle(self.PIN_ID_1, self.MAX_PWM)
        self.io.set_PWM_dutycycle(self.PIN_ID_2, self.MAX_PWM)

    def init_PWM(self, FREQ):
        # Set up the four pins as output (OUTPUT MODE).
        self.io.set_mode(self.PIN_ID_1, pigpio.OUTPUT)
        self.io.set_mode(self.PIN_ID_2, pigpio.OUTPUT)

        # Prepare the PWM and sets PWM range to 255. The range gives the 
        # maximum value for 100% duty cycle.
        self.io.set_PWM_range(self.PIN_ID_1, self.MAX_PWM)
        self.io.set_PWM_range(self.PIN_ID_2, self.MAX_PWM)

        # Set the PWM frequency to 1000Hz.
        self.io.set_PWM_frequency(self.PIN_ID_1, FREQ)
        self.io.set_PWM_frequency(self.PIN_ID_2, FREQ)
    
    # Depending on if setlevel is positive or negative, sends a singal to each respective
    # pin (one pin being at that level and the other at its corresponding magnitude).
    # If neither is the case (setlevel is 0), then motor stops. 
    def setlevel(self, level):
        if abs(level) > 1:
            return -1

        if level > 0:
            pin1_duty = self.MAX_PWM
            pin2_duty = self.MAX_PWM - level * (self.MAX_PWM - self.MAX_DELTA)
        else:
            pin1_duty = self.MAX_PWM + level * (self.MAX_PWM - self.MAX_DELTA)
            pin2_duty = self.MAX_PWM

        self.io.set_PWM_dutycycle(self.PIN_ID_1, pin1_duty)
        self.io.set_PWM_dutycycle(self.PIN_ID_2, pin2_duty)

    # sets both PWM duty cycles to 0, which disconnects/de-energizes the motor
    # Clear the PINs (commands).
    def off(self):
        self.io.set_PWM_dutycycle(self.PIN_ID_1, 0)
        self.io.set_PWM_dutycycle(self.PIN_ID_2, 0)

# Defining LEFT and RIGHT with constant values for for loop
class Directions(Enum):
    LEFT = -1
    RIGHT = 1

# Defining for each STYLE with constant values for for loop
class Styles(Enum):
    STRAIGHT = 0
    VEER = 1
    STEER = 2
    TURN = 3
    HOOK = 4
    SPIN = 5

# Dictionary/Look up table that has the tuned setlevel values for each motor and sets their behavior 
# for each direction and style. 
# While STRAIGHT doesn't have a direction, we had to add (Right, Straight) and (Left, Straight) for the 
# nested for loop in flower_power.py that goes through each direction and style.
# However, a nested if statment accounts for this and ignores the additonal STRAIGHT keys in the dictionary
# and only goes straight once. 

class DriveSystem:
    DRIVE_DICT = {

        # STRAIGHT 
        (None, Styles.STRAIGHT) : [0.68, 0.68],
        (Directions.RIGHT, Styles.STRAIGHT) : [0.68, 0.68],
        (Directions.LEFT, Styles.STRAIGHT) : [0.68, 0.68],

        #RIGHT TURNS 
        (Directions.RIGHT, Styles.VEER) : [0.78, 0.68],
        (Directions.RIGHT, Styles.STEER) : [0.79, 0.63],
        (Directions.RIGHT, Styles.TURN) : [0.80, 0.47],
        (Directions.RIGHT, Styles.HOOK) : [0.80, 0],
        (Directions.RIGHT, Styles.SPIN) : [0.66, -0.66],

        #LEFT TURNS 
        (Directions.LEFT, Styles.VEER) : [0.69, 0.78],
        (Directions.LEFT, Styles.STEER) : [0.63, 0.79],
        (Directions.LEFT, Styles.TURN) : [0.47, 0.80],
        (Directions.LEFT, Styles.HOOK) : [0.0, 0.77],
        (Directions.LEFT, Styles.SPIN) : [-0.66, 0.66],
        }
    
    # Initializing the motors and setting motor pins for signals 
    def __init__(self, io, pin1_left, pin2_left, pin1_right, pin2_right):
        self.left_motor = Motor(io, pin1_left, pin2_left)
        self.right_motor = Motor(io, pin1_right, pin2_right)

    # Inputting corresponding setlevel()s for each motor depending on which 
    # style and direction is inputted in reference to which key in the DRIVE_DICT.
    # The value of the corresponding keys is as a tuple is inputted into the motors 
    def drive(self, style, direction):
        motor_powers = self.DRIVE_DICT[(direction, style)]

        self.left_motor.setlevel(motor_powers[0])
        self.right_motor.setlevel(motor_powers[1])

    # motors charged but stopped (no rotational output)
    def brake(self):
        self.left_motor.setlevel(0)
        self.right_motor.setlevel(0)

    # motors discharged and completely off 
    def deactivate(self):
        self.left_motor.off()
        self.right_motor.off()
