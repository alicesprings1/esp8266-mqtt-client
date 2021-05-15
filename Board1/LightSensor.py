from machine import Pin 
from config import Config
import uasyncio
import json

class LS(Config):
    async def get_data(self):
        self.p=Pin(self.pin,Pin.IN)
        light=self.p.value()
        return json.dumps({'light':light})

if __name__=='__main__':
    ls001=LS(pin=4)
    data=uasyncio.run(ls001.get_data())
    print(data)