import sys
import pi_utilities
import pigpio
import Motor
import time

PIN_LEFT_MOTOR_1 = 5
PIN_LEFT_MOTOR_2 = 6

PIN_RIGHT_MOTOR_1 = 7
PIN_RIGHT_MOTOR_2 = 8

io = pigpio.pi()
pi_utilities.setup_gpio_connection(io)

left_motor = Motor.Motor(io, PIN_LEFT_MOTOR_1, PIN_LEFT_MOTOR_2, 50)
right_motor = Motor.Motor(io, PIN_RIGHT_MOTOR_1, PIN_RIGHT_MOTOR_2, 50)


left_motor.setlevel(0.5)
right_motor.setlevel(-0.5)
time.sleep(0.95)


left_motor.off()
right_motor.off()
io.stop()