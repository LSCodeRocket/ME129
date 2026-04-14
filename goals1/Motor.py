import utilities
import pigpio
import sys

class Motor:
    def __init__(self, io_object, PIN_ID_1, PIN_ID_2, MAX_DELTA):
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

        # Set up the four pins as output (OUTPUT MODE).
        self.io.set_mode(self.PIN_ID_1, pigpio.OUTPUT)
        self.io.set_mode(self.PIN_ID_2, pigpio.OUTPUT)

        # Prepare the PWM and sets PWM range to 255. The range gives the 
        # maximum value for 100% duty cycle.
        self.io.set_PWM_range(self.PIN_ID_1, self.MAX_PWM)
        self.io.set_PWM_range(self.PIN_ID_2, self.MAX_PWM)

        # Set the PWM frequency to 1000Hz.
        self.io.set_PWM_frequency(self.PIN_ID_1, 1000)
        self.io.set_PWM_frequency(self.PIN_ID_2, 1000)

        # initializes the motor to stop (both pins at 255) 
        # Set all pins to their maximum value, which turns on motor
        # driver but has no effective output (brake).
        self.io.set_PWM_dutycycle(self.PIN_ID_1, self.MAX_PWM)
        self.io.set_PWM_dutycycle(self.PIN_ID_2, self.MAX_PWM)
    
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

        self.io.set_PWM_dutycycle(self.PIN_ID_1, int(pin1_duty))
        self.io.set_PWM_dutycycle(self.PIN_ID_2, int(pin2_duty))
        print(f"Duty 1: {int(pin1_duty)}, Duty 2: {int(pin2_duty)}")

    # sets both PWM duty cycles to 0, which disconnects/de-energizes the motor
    # Clear the PINs (commands).
    def off(self):
        self.io.set_PWM_dutycycle(self.PIN_ID_1, 0)
        self.io.set_PWM_dutycycle(self.PIN_ID_2, 0)