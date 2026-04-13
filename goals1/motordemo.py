#!/usr/bin/env python3
#
#   motordemo.py
#
#   This shows how to interface with the GPIO (general purpose I/O)
#   pins and how to drive the PWM for the motors.  Please use as an
#   example, but change to suit the goals!
#

# Imports
import pigpio
import sys
import time
import traceback

# Define the motor pins.
PIN_MOTORR_LEGA = 7             # Motor Right Leg A
PIN_MOTORR_LEGB = 8             # Motor Right Leg B (reverse)

PIN_MOTORL_LEGA = 6             # Motor Left  Leg A
PIN_MOTORL_LEGB = 5             # Motor Left  Leg B (reverse)


#
#   Main
#
if __name__ == "__main__":

    ############################################################
    # Prepare the GPIO interface/connection (to command the motors).
    print("Setting up the GPIO...")
    io = pigpio.pi()
    if not io.connected:
        print("Unable to connection to pigpio daemon!")
        sys.exit(0)
    print("GPIO ready...")

    # Set up the four pins as output (commanding the motors).
    io.set_mode(PIN_MOTORR_LEGA, pigpio.OUTPUT)
    io.set_mode(PIN_MOTORR_LEGB, pigpio.OUTPUT)
    io.set_mode(PIN_MOTORL_LEGA, pigpio.OUTPUT)
    io.set_mode(PIN_MOTORL_LEGB, pigpio.OUTPUT)

    # Prepare the PWM.  The range gives the maximum value for 100%
    # duty cycle, using integer commands (1 up to max).
    io.set_PWM_range(PIN_MOTORR_LEGA, 255)
    io.set_PWM_range(PIN_MOTORR_LEGB, 255)
    io.set_PWM_range(PIN_MOTORL_LEGA, 255)
    io.set_PWM_range(PIN_MOTORL_LEGB, 255)
    
    # Set the PWM frequency to 1000Hz.
    io.set_PWM_frequency(PIN_MOTORR_LEGA, 1000)
    io.set_PWM_frequency(PIN_MOTORR_LEGB, 1000)
    io.set_PWM_frequency(PIN_MOTORL_LEGA, 1000)
    io.set_PWM_frequency(PIN_MOTORL_LEGB, 1000)

    # Set all pins to their maximum value, which enables the motor
    # driver but asks for no effective output.
    io.set_PWM_dutycycle(PIN_MOTORR_LEGA, 255)
    io.set_PWM_dutycycle(PIN_MOTORR_LEGB, 255)
    io.set_PWM_dutycycle(PIN_MOTORL_LEGA, 255)
    io.set_PWM_dutycycle(PIN_MOTORL_LEGB, 255)

    print("Motors ready...")

    ############################################################
    # Drive.
    # Place this is a try-except structure, so we can turn off the
    # motors even if the code crashes.
    try:
        # Example 1: Drive right motor forward/backward.
        print("Driving right motor forward, stopping, then reversing...")
        io.set_PWM_dutycycle(PIN_MOTORR_LEGA, 255)
        io.set_PWM_dutycycle(PIN_MOTORR_LEGB, 100)
        time.sleep(1)

        io.set_PWM_dutycycle(PIN_MOTORR_LEGA, 255)
        io.set_PWM_dutycycle(PIN_MOTORR_LEGB, 255)
        time.sleep(1)

        io.set_PWM_dutycycle(PIN_MOTORR_LEGA, 100)
        io.set_PWM_dutycycle(PIN_MOTORR_LEGB, 255)
        time.sleep(1)

        io.set_PWM_dutycycle(PIN_MOTORR_LEGA, 255)
        io.set_PWM_dutycycle(PIN_MOTORR_LEGB, 255)
        time.sleep(1)

        # Example 2: Ramp left motor (forward) up/down.
        print("Ramping left motor (forward) up/down...") 
        pinA = PIN_MOTORL_LEGA
        pinB = PIN_MOTORL_LEGB

        for delta in [63, 127, 191, 255, 191, 127, 63, 0]:
            pwmA = 255
            pwmB = 255-delta

            print("Pin %d at level %3d, Pin %d at level %3d" %
                  (pinA, pwmA, pinB, pwmB))
            io.set_PWM_dutycycle(pinA, pwmA)
            io.set_PWM_dutycycle(pinB, pwmB)
            time.sleep(1)

    except BaseException as ex:
        # Report the error, but continue with the normal shutdown.
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()

    ############################################################
    # Turn Off.
    # Note the PWM will stay at the last commanded value.  So you want
    # to be sure to set to zero before the program closes.  Else your
    # robot will run away...
    print("Turning off...")

    # Clear the PINs (commands).
    io.set_PWM_dutycycle(PIN_MOTORR_LEGA, 0)
    io.set_PWM_dutycycle(PIN_MOTORR_LEGB, 0)
    io.set_PWM_dutycycle(PIN_MOTORL_LEGA, 0)
    io.set_PWM_dutycycle(PIN_MOTORL_LEGB, 0)
    
    # Also stop the interface.
    io.stop()
