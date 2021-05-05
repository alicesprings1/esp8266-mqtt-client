from machine import ADC
from config import Config
import uasyncio
import json

class YL69(Config):
    async def get_data(self):
        adc=ADC(0)
        soil_hum=adc.read()
        soil_hum=100*(1-soil_hum/1024)
        return json.dumps({'soil_hum':soil_hum})

if __name__=='__main__':
    yl69=YL69()
    data=uasyncio.run(yl69.get_data())
    print(data)