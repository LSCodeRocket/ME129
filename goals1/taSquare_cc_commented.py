import pigpio
import sys
import time
import traceback

# Stores the two gpio pin numbers for the Right motor's leads
PIN_MOTORR_LEGA = 7
PIN_MOTORR_LEGB = 8

# Stores the two gpio pin numbers for the Left motor's leads
PIN_MOTORL_LEGA = 5
PIN_MOTORL_LEGB = 6

class Motor:
    def __init__(self, io, pinLegA, pinLegB, MAX_DELTA):
        # Create the shared io.pi() io object once 
        # Create two separate motor objects with its each pin numbers 
        # pinLegA : gpio pin number for Leg A (forward lead)
        # pinLegB : gpio pin number for Leg B (backwards lead)
        self.io   = io
        self.pinA = pinLegA
        self.pinB = pinLegB
        self.MAX_DELTA = MAX_DELTA

        # Set up the four pins as output (OUTPUT MODE).
        self.io.set_mode(self.pinA, pigpio.OUTPUT)
        self.io.set_mode(self.pinB, pigpio.OUTPUT)

        # Prepare the PWM and sets PWM range to 255. The range gives the 
        # maximum value for 100% duty cycle.
        self.io.set_PWM_range(self.pinA, 255)
        self.io.set_PWM_range(self.pinB, 255)

        # Set the PWM frequency to 1000Hz.
        self.io.set_PWM_frequency(self.pinA, 1000)
        self.io.set_PWM_frequency(self.pinB, 1000)

        # initializes the motor to stop (both pins at 255) 
        # Set all pins to their maximum value, which turns on motor
        # driver but has no effective output (brake).
        self.io.set_PWM_dutycycle(self.pinA, 255)
        self.io.set_PWM_dutycycle(self.pinB, 255)

    # sets both PWM duty cycles to 0, which disconnects/de-energizes the motor
    # Clear the PINs (commands).
    def off(self):
        self.io.set_PWM_dutycycle(self.pinA, 0)
        self.io.set_PWM_dutycycle(self.pinB, 0)

    # Depending on if setlevel is positive or negative, sends a singal to each respective
    # pin (one pin being at that level and the other at its corresponding magnitude).
    # If neither is the case (setlevel is 0), then motor stops. 
    def setlevel(self, level):
        # Forward: pinA stays at 255, pinB is reduced
        if level > 0:
            self.io.set_PWM_dutycycle(self.pinA, 255)
            self.io.set_PWM_dutycycle(self.pinB, 255 - int(level * (255 - self.MAX_DELTA)))

        # Backward: pinB stays at 255, pinA is reduced
        elif level < 0:
            self.io.set_PWM_dutycycle(self.pinA, 255 - int(abs(level) * (255 - self.MAX_DELTA)))
            self.io.set_PWM_dutycycle(self.pinB, 255)

        # Stop/brake: both pins at 255, motor energized but not moving
        else:
            self.io.set_PWM_dutycycle(self.pinA, 255)
            self.io.set_PWM_dutycycle(self.pinB, 255)

if __name__ == "__main__":
    # initialize motorRight = Motor(io, pinMotorRightLegA, pinMotorRightLegB)
    # and motorLeft = Motor(io, pinMotorLeftLegA, pinMotorLeftLegB)
    io = pigpio.pi()
    motorR = Motor(io, PIN_MOTORR_LEGA, PIN_MOTORR_LEGB)
    motorL = Motor(io, PIN_MOTORL_LEGA, PIN_MOTORL_LEGB)

    # driving code in try/except
    try:
        # Each loop is for one side and one turn (x 4 creates a full square path). 
        for side in range(4):

            # Drive forward 1 meter (motorR and motorL values adjusted for drifting)
            motorR.setlevel(0.97)
            motorL.setlevel(1)
            time.sleep(1.87)

            # Brake
            motorR.setlevel(0)
            motorL.setlevel(0)
            time.sleep(1)

            # Turn 90 degrees in place by sending the right motor backward and left motor 
            # forward with both motors at the same magnitude of speed (abs(level)). 
            motorR.setlevel(0.5)
            motorL.setlevel(-0.5)
            time.sleep(0.58)

            # Brake
            motorR.setlevel(0)
            motorL.setlevel(0)
            time.sleep(1)

    # Except: print error 
    except BaseException as ex:
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()

    # motorR.off(), motorL.off(), and io.stop() to make sure motors don't spin forever 
    motorR.off()
    motorL.off()
    io.stop()