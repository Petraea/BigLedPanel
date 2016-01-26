import serial
import time

class Ledboard:
    def __init__(self,port,speed):
        self.ser=None
        self.port=port
        self.speed=speed
        self.framebuffer = [0x00] * 90
        time.sleep(1)
        self.connect()

    def connect(self):
        self.ser = serial.Serial(self.port, self.speed, timeout=1)

    def disconnect(self):
        self.ser.flush()
        self.ser.close()
        self.ser = None

    def writebuffer(self, data):
        if len(data) == 90:
            self.framebuffer = data
            try:
                self.draw() 
            except:
                pass

    def drawstring(self, string, font):
        i = 0
        self.framebuffer = [0x00] * 90
        for char in string:
            self.framebuffer[i] = font[ord(char)-32][0]
            i += 1
            self.framebuffer[i] = font[ord(char)-32][1]
            i += 1
            self.framebuffer[i] = font[ord(char)-32][2]
            i += 1
            self.framebuffer[i] = font[ord(char)-32][3]
            i += 1 
            self.framebuffer[i] = font[ord(char)-32][4]
            i += 1 
        try:
            self.draw() 
        except:
            pass
 
    def draw(self):
        if self.ser is None:
            self.connect()
        self.ser.write(chr(0x81))
        self.ser.write(chr(0x80))
        for frame in self.framebuffer:
            while self.ser.outWaiting() > 0:
                time.sleep(0.5)
            self.ser.write(chr(frame))
#        time.sleep(.20)
        self.ser.flush()

    def demo(self):
        for i in range(0,89):
            self.framebuffer[i]=i
        self.draw()
