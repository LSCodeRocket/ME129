import DriveSystem
import pigpio
import sys
import LineSensor

import time

def run_flower_power(drive, sensor):
    t = time.time()

    # Start with STRAIGHT style.
    drive.drive(DriveSystem.Styles.STRAIGHT, None)
    
    # Robot drives and compounds time until reaches 4 seconds, then robot stops. 
    while time.time() <= t + 4:
        print(time.time())
    drive.brake()
    
    # Waits for relocation and moves on when "return" is pressed.
    input("Replaced?")

    # Goes through each STYLE in each DIRECTION.
    for dir in list(DriveSystem.Directions):
        for style in list(DriveSystem.Styles):

            # ignores additional STRAIGHTS in DRIVE_DICT that were added for the nested
            # for loop logic, so robot only goes STRAIGHT once. 
            if style == DriveSystem.Styles.STRAIGHT:
                continue 
            
            # Robot drives and compounds time until reaches 4 seconds, then robot stops.
            t = time.time()
            while time.time() <= t + 4:
                drive.drive(style, dir)
                print(time.time())
            drive.brake()

            # Waits for relocation and moves on when "return" is pressed.
            input("Replaced?")

    

# Motor Pins
PIN_LEFT_MOTOR_1 = 6
PIN_LEFT_MOTOR_2 = 5
PIN_RIGHT_MOTOR_1 = 8
PIN_RIGHT_MOTOR_2 = 7

# IR sensor Pins (L, M, R)
PIN_LEFT_IR = 18
PIN_MIDDLE_IR = 15
PIN_RIGHT_IR = 14

io = pigpio.pi()
if not io.connected:
    print("Unable to connect.")
    sys.exit(0)

print("GPIO READY!")

drive = DriveSystem.DriveSystem(io, PIN_LEFT_MOTOR_1, PIN_LEFT_MOTOR_2, PIN_RIGHT_MOTOR_1, PIN_RIGHT_MOTOR_2)
sensor = LineSensor.LineSensor( io, PIN_LEFT_IR, PIN_MIDDLE_IR, PIN_RIGHT_IR)

# Flower Power in try/except block to make sure motor doesn't spin forever when 
# the call to the function is stopped 

try:
    run_flower_power(drive, sensor)
except:
    drive.deactivate()
    io.stop()
    sys.exit(0)

drive.deactivate()
io.stop()
