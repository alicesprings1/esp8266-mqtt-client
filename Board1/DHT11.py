import machine
import dht
import uasyncio
import json
from config import Config

class DHT11(Config):

    async def get_data(self):
        d=dht.DHT11(machine.Pin(self.pin))
        d.measure()
        return json.dumps({'temperature':d.temperature(),'humidity':d.humidity()})

if __name__=='__main__':
    dht11=DHT11(pin=2)
    data=uasyncio.run(dht11.get_data())
    print(data)