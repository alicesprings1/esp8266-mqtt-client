from machine import Pin 
from config import Config
import uasyncio
import json

class LS(Config):
    def __init__(self,client_id,**kw):
        super().__init__(client_id,**kw)
        if 'pin' in kw:
            self.pin=Pin(kw['pin'],Pin.IN)

    async def get_data(self):
        light=self.pin.value()
        return json.dumps({'light':light})

if __name__=='__main__':
    ls001=LS('LS_001',pin=4)
    data=uasyncio.run(ls001.get_data())
    print(ls001.client_id)
    print(data)