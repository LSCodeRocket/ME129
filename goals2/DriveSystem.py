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

        self.set_PWM_dutycycles(self.MAX_PWM, self.MAX_PWM)

    def set_PWM_dutycycles(self, duty1, duty2):
        # initializes the motor to stop (both pins at 255) 
        # Set all pins to their maximum value, which turns on motor
        # driver but has no effective output (brake).
        self.io.set_PWM_dutycycle(self.PIN_ID_1, duty1)
        self.io.set_PWM_dutycycle(self.PIN_ID_2, duty2)

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
        # print(f"Duty 1: {int(pin1_duty)}, Duty 2: {int(pin2_duty)}")

    # sets both PWM duty cycles to 0, which disconnects/de-energizes the motor
    # Clear the PINs (commands).
    def off(self):
        self.io.set_PWM_dutycycle(self.PIN_ID_1, 0)
        self.io.set_PWM_dutycycle(self.PIN_ID_2, 0)


class Directions(Enum):
    LEFT = -1
    RIGHT = 1

class Styles(Enum):
    STRAIGHT = 0
    VEER = 1
    STEER = 2
    TURN = 3
    HOOK = 4
    SPIN = 5

class DriveSystem:
    DRIVE_DICT = {
        (None, Styles.STRAIGHT) : [0.65, 0.65],
        (Directions.RIGHT, Styles.VEER) : [0.77, 0.67*1.08],
        (Directions.RIGHT, Styles.STRAIGHT) : [0.92, 1],
        (Directions.RIGHT, Styles.STRAIGHT) : [0.92, 1],
        }
    
    
    def __init__(self, io, pin1_left, pin2_left, pin1_right, pin2_right):
        self.left_motor = Motor(io, pin1_left, pin2_left)
        self.right_motor = Motor(io, pin1_right, pin2_right)

    def drive(self, style, direction):
        motor_powers = self.DRIVE_DICT[(direction, style)]

        self.left_motor.setlevel(motor_powers[0])
        self.right_motor.setlevel(motor_powers[1])

    
    def brake(self):
        self.left_motor.setlevel(0)
        self.right_motor.setlevel(0)

    def deactivate(self):
        self.left_motor.off()
        self.right_motor.off()