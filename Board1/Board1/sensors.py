import time
import json
import uasyncio
from YL69 import YL69
from DHT11 import DHT11
from LightSensor import LS
from simple import MQTTClient


def create_client(device):
    return MQTTClient(device.client_id,device.server,device.port,device.user,device.password,keepalive=60)

def initialize():
    devices=[]

    DHT11_001=DHT11('DHT11_001',pin=2)
    DHT11_001.pub_topic='/DHT11/{}/report-property'.format(DHT11_001.client_id)
    DHT11_001.client=create_client(DHT11_001)
    devices.append(DHT11_001)

    YL69_001=YL69('YL69_001')
    YL69_001.pub_topic='/YL69/{}/report-property'.format(YL69_001.client_id)
    YL69_001.client=create_client(YL69_001)
    devices.append(YL69_001)

    LS_001=LS('LS_001',pin=4)
    LS_001.pub_topic='/LS/{}/report-property'.format(LS_001.client_id)
    LS_001.client=create_client(LS_001)
    devices.append(LS_001)
        
    return devices
    
def connect_all(devices):
    for device in devices:
        device.client.connect()

def disconnect_all(devices):
    for device in devices:
        device.client.disconnect()

async def pub(device):
    payload=await uasyncio.wait_for(device.get_data(),None)
    device.client.publish(device.pub_topic,payload)
    print('{} published to topic {}'.format(device.client_id,device.pub_topic))

async def main(devices):
    
    while True:
        for device in devices:
            uasyncio.create_task(pub(device))
        await uasyncio.sleep(5)

def upload_data():
    try:
        devices=initialize()
        connect_all(devices)
        uasyncio.run(main(devices))
    finally:
        disconnect_all(devices)

if __name__=='__main__':
    upload_data()
    