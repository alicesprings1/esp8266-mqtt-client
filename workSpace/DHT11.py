import machine
import dht
import uasyncio
import json
from config import Config

class DHT11(Config):
    def __init__(self,pin):
        self.pin=pin

    async def get_data(self):
        d=dht.DHT11(machine.Pin(self.pin))
        d.measure()
        return json.dumps({'temperature':d.temperature(),'humidity':d.humidity()})
        # return d.temperature(),d.humidity()

if __name__=='__main__':
    dht11=DHT11(2)
    temp,hum=uasyncio.run(dht11.get_data())
    print(temp,hum)