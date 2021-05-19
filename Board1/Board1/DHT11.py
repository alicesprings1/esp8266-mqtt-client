import machine
import dht
import uasyncio
import json
from config import Config

# DHT11.py
class DHT11(Config):
    def __init__(self,client_id,**kw):
        super().__init__(client_id,**kw)
        if 'pin' in kw:
            self.pin=dht.DHT11(machine.Pin(kw['pin']))
    # async关键字定义协程函数get_data()
    async def get_data(self):
        self.pin.measure()
        return json.dumps({'temperature':self.pin.temperature(),'humidity':self.pin.humidity()})

if __name__=='__main__':
    dht11=DHT11('DHT11_001',pin=2)
    data=uasyncio.run(dht11.get_data())
    print(dht11.client_id)
    print(data)


