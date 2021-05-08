from config import Config
from machine import Pin
import time

class LED(Config):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.p=Pin(self.pin,Pin.OUT)
    
    def shine(self,status):
        if status=='on':
            self.p.on()
        elif status=='off':
            self.p.off()
        else:
            pass

if __name__=='__main__':
    red=LED(pin=14)
    red.shine('on')
    time.sleep(1)
    red.shine('off')