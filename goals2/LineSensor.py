class IR:
    def __init__(self, io, pin):
        self.pin = pin
        self.io = io

    def read(self):
        return self.io.read(self.pin)
    

class LineSensor:
    def __init__(self, io, pin1, pin2, pin3):
        self.IR_1 = IR(io, pin1)
        self.IR_2 = IR(io, pin2)
        self.IR_3 = IR(io, pin3)

    def read(self):
        return (self.IR_1.read(), self.IR_2.read(), self.IR_3.read())