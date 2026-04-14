import pigpio
import sys
import traceback
import DriveSystem
import LineSensor

PIN_LEFT_MOTOR_1 = 6
PIN_LEFT_MOTOR_2 = 5
PIN_RIGHT_MOTOR_1 = 8
PIN_RIGHT_MOTOR_2 = 7

PIN_IR_LEFT   = 18
PIN_IR_MIDDLE = 15
PIN_IR_RIGHT  = 14

FEEDBACK_LAW = {
    (0, 1, 0) : (None,                        DriveSystem.Styles.STRAIGHT),  # Centered
    (0, 1, 1) : (DriveSystem.Directions.RIGHT, DriveSystem.Styles.TURN),    # Slight Left
    (0, 0, 1) : (DriveSystem.Directions.RIGHT, DriveSystem.Styles.HOOK),     # Far Left
    (1, 1, 0) : (DriveSystem.Directions.LEFT,  DriveSystem.Styles.TURN),    # Slight Right
    (1, 0, 0) : (DriveSystem.Directions.LEFT,  DriveSystem.Styles.HOOK),     # Far Right
    (0, 0, 0) : None,                                                          # Off tape -> stop
    (1, 1, 1) : (None, DriveSystem.Styles.STRAIGHT),  # All on straight
    (1, 0, 1) : (None, DriveSystem.Styles.STRAIGHT),  # Unlikely straight
}

def turn_around(drive, sensor):

    drive.drive(DriveSystem.Styles.SPIN, DriveSystem.Directions.RIGHT)

    while True: 
        reading = sensor.read()
        if reading != (0, 0, 0):
            return


def run(drive, sensor):
    while True:
        reading = sensor.read()
        action = FEEDBACK_LAW[reading]

        if action is None:
            current_average = sensor.get_average()

            if current_average == [0, 1, 0]:
                turn_around(drive, sensor)
            elif current_average[2] == 1:
                drive.drive(DriveSystem.Styles.VEER, DriveSystem.Directions.RIGHT)
            elif current_average[0] == 1:
                drive.drive(DriveSystem.Styles.VEER, DriveSystem.Directions.LEFT)
            else:
                turn_around(drive, sensor)
            
        else:
            direction, style = action
            drive.drive(style, direction)

def main():
    io = pigpio.pi()
    if not io.connected:
        print("Unable to connect to pigpio")
        sys.exit(0)
    print("GPIO ready!")

    drive = DriveSystem.DriveSystem(io, PIN_LEFT_MOTOR_1, PIN_LEFT_MOTOR_2,PIN_RIGHT_MOTOR_1, PIN_RIGHT_MOTOR_2)
    sensor = LineSensor.LineSensor(io, PIN_IR_LEFT, PIN_IR_MIDDLE, PIN_IR_RIGHT)

    try:
        run(drive, sensor)
    except BaseException as ex:
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()

    #shutdown cleanly
    drive.deactivate()
    io.stop()

if __name__ == "__main__":
    main()