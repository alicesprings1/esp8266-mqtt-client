from config import Config
from machine import Pin
import time

class LED(Config):
    def __init__(self,client_id,**kw):
        super().__init__(client_id,**kw)
        if 'pin' in kw:
            self.pin=Pin(kw['pin'],Pin.OUT)
    
    def shine(self,status):
        if status=='on':
            self.pin.on()
        elif status=='off':
            self.pin.off()
        else:
            pass

if __name__=='__main__':
    red=LED('red',pin=14)
    print(red.client_id)
    red.shine('on')
    time.sleep(1)
    red.shine('off')