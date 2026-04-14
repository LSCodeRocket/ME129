# Initializing IR sensors and setting pins
class IR:
    def __init__(self, io, pin):
        self.pin = pin
        self.io = io

    # calls read() to output what the sensor sees
    def read(self):
        return self.io.read(self.pin)
    

# Initializing IR sensors and setting pins for each (L, M, R)
# BUFFER_LENGTH sets how many previous readings we want to look at before 
# a certain behavior (how long the list of previous readings is going to be)
class LineSensor:
    def __init__(self, io, pin1, pin2, pin3, BUFFER_LENGTH = 10):
        self.IR_1 = IR(io, pin1)
        self.IR_2 = IR(io, pin2)
        self.IR_3 = IR(io, pin3)
        self.buffer = [] 
        self.BUFFER_LENGTH = BUFFER_LENGTH

    def read(self):
        reading = (self.IR_1.read(), self.IR_2.read(), self.IR_3.read())

        # if robot is completely off the line, don't add to buffer list 
        if reading == (0, 0, 0):
            return reading

        # append all other readings to buffer list
        self.buffer.append(reading)

        # Once buffer list reaches the max amount of readings we want, pop the first reading
        if len(self.buffer) > self.BUFFER_LENGTH:
            self.buffer.pop(0)
        else:
            return reading

        return reading 

    # How often did each sensor read white/black 
    # Measure each sensor's detection, for "off the line" behavior to differenciate between when 
    # pushed off the line versus reached end of the line 

    def get_average(self, threshold = 0.1):
        total = [0, 0, 0]
        
        if len(self.buffer) == 0:
            return [0, 0, 0]
        
        # adds all the readings for each sensor and stores as a tuple
        for i in range(len(self.buffer)):
            for j in range(3):
                total[j] += self.buffer[i][j]

        # takes the average of each coordinate (average readings for each sensor)
        # Did it see black majority of the time or white?
        average = [0, 0, 0]
        for i in range(3):
            # only make average 1 if it sees it for more than thresshold
            if total[i]/len(self.buffer) >= threshold:
                average[i] = 1

        return average