import sys

def setup_gpio_connection(io_object):
    if not io_object.connected:
        print("Unable to connect.")
        sys.exit(0)
    print("GPIO READY!")
