class IR:
    def __init__(self, io, pin):
        self.pin = pin
        self.io = io

    def read(self):
        return self.io.read(self.pin)
    

class LineSensor:
    def __init__(self, io, pin1, pin2, pin3, BUFFER_LENGTH = 10):
        self.IR_1 = IR(io, pin1)
        self.IR_2 = IR(io, pin2)
        self.IR_3 = IR(io, pin3)
        self.buffer = [] 
        self.BUFFER_LENGTH = BUFFER_LENGTH

    def read(self):
        reading = (self.IR_1.read(), self.IR_2.read(), self.IR_3.read())

        self.buffer.append(reading)
        if len(self.buffer) > self.BUFFER_LENGTH:
            self.buffer.pop(0)

        return reading 

    def get_average(self):
        return [round(sum([self.buffer[i][j] for i in range(len(self.buffer))])/len(self.buffer)) for j in range(3)]
