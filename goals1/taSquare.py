import pigpio
import sys
import time
import traceback


PIN_MOTORR_LEGA = 7
PIN_MOTORR_LEGB = 8

PIN_MOTORL_LEGA = 5
PIN_MOTORL_LEGB = 6

class Motor:
    def __init__(self, io, pinLegA, pinLegB):
        self.io   = io
        self.pinA = pinLegA
        self.pinB = pinLegB

        self.io.set_mode(self.pinA, pigpio.OUTPUT)
        self.io.set_mode(self.pinB, pigpio.OUTPUT)

        self.io.set_PWM_range(self.pinA, 255)
        self.io.set_PWM_range(self.pinB, 255)

        self.io.set_PWM_frequency(self.pinA, 1000)
        self.io.set_PWM_frequency(self.pinB, 1000)

        self.io.set_PWM_dutycycle(self.pinA, 255)
        self.io.set_PWM_dutycycle(self.pinB, 255)

    def off(self):
        self.io.set_PWM_dutycycle(self.pinA, 0)
        self.io.set_PWM_dutycycle(self.pinB, 0)

    def setlevel(self, level):
        if level > 0:
            self.io.set_PWM_dutycycle(self.pinA, 255)
            self.io.set_PWM_dutycycle(self.pinB, 255 - int(level * 255))

        elif level < 0:
            self.io.set_PWM_dutycycle(self.pinA, 255 - int(abs(level) * 255))
            self.io.set_PWM_dutycycle(self.pinB, 255)

        else:
            self.io.set_PWM_dutycycle(self.pinA, 255)
            self.io.set_PWM_dutycycle(self.pinB, 255)

if __name__ == "__main__":
    print("Setting up the GPIO...")
    io = pigpio.pi()
    if not io.connected:
        print("Unable to connect to pigpio daemon!")
        sys.exit(0)
    print("GPIO ready.")

    motorR = Motor(io, PIN_MOTORR_LEGA, PIN_MOTORR_LEGB)
    motorL = Motor(io, PIN_MOTORL_LEGA, PIN_MOTORL_LEGB)
    print("Motors ready.")

    #DRIVE_LEVEL = 0.3
    #DRIVE_TIME  = 2.0

    #TURN_LEVEL  = 0.5
    #TURN_TIME   = 0.85

    try:
        for side in range(4):
            motorR.setlevel(0.93)
            motorL.setlevel(0.95)
            time.sleep(1.4)

            motorR.setlevel(0)
            motorL.setlevel(0)
            time.sleep(1)

            motorR.setlevel(-0.5)
            motorL.setlevel(0.5)
            time.sleep(0.63)

            motorR.setlevel(0)
            motorL.setlevel(0)
            time.sleep(1)

        print("Square complete!")

    except BaseException as ex:
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()

    print("Turning off...")
    motorR.off()
    motorL.off()
    io.stop()