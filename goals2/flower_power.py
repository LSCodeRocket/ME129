import DriveSystem
import pigpio
import sys
import LineSensor

import time

def run_flower_power(drive, sensor):
    t = time.time()
    drive.drive(DriveSystem.Styles.STRAIGHT, None)
    while time.time() <= t + 4:
        print(time.time())

    drive.brake()
    input("Replaced?")

    for dir in list(DriveSystem.Directions):
        for style in list(DriveSystem.Styles):
            t = time.time()
            while time.time() <= t + 4:
                drive.drive(style, dir)
                print(time.time())
            drive.brake()
            input("Replaced?")

    


PIN_LEFT_MOTOR_1 = 6
PIN_LEFT_MOTOR_2 = 5
PIN_RIGHT_MOTOR_1 = 8
PIN_RIGHT_MOTOR_2 = 7

PIN_LEFT_IR = 14
PIN_MIDDLE_IR = 15
PIN_RIGHT_IR = 18



io = pigpio.pi()
if not io.connected:
    print("Unable to connect.")
    sys.exit(0)

print("GPIO READY!")

drive = DriveSystem.DriveSystem(
    io, PIN_LEFT_MOTOR_1, PIN_LEFT_MOTOR_2,
    PIN_RIGHT_MOTOR_1, PIN_RIGHT_MOTOR_2
)

sensor = LineSensor.LineSensor(
    io, PIN_LEFT_IR, PIN_MIDDLE_IR, PIN_RIGHT_IR)

try:
    run_flower_power(drive, sensor)
except:
    drive.deactivate()
    io.stop()
    sys.exit(0)

drive.deactivate()
io.stop()
