from machine import ADC
from config import Config
import uasyncio
import json

class RainSensor(Config):
    async def get_data(self):
        adc=ADC(0)
        rain_drop=adc.read()
        rain_drop=100*(1-rain_drop/1024)
        return json.dumps({'rain_drop':rain_drop})

if __name__=='__main__':
    rain_sensor=RainSensor()
    data=uasyncio.run(rain_sensor.get_data())
    print(data)