from machine import ADC
from config import Config
import json

class RainSensor(Config):
    def __init__(self, client_id):
        super().__init__(client_id)

    def get_data(self):
        adc=ADC(0)
        rain_drop=adc.read()
        rain_drop=100*(1-rain_drop/1024)
        return json.dumps({'rain_drop':rain_drop})

if __name__=='__main__':
    rain_sensor=RainSensor('RS_001')
    data=rain_sensor.get_data()
    print(rain_sensor.client_id)
    print(data)