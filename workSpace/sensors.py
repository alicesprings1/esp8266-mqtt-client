import time
import json
import uasyncio
from YL69 import YL69
from DHT11 import DHT11
from simple import MQTTClient


def create_client(device):
    return MQTTClient(device.client_id,device.server,device.port,device.user,device.password)

def initialize():
    devices=[]

    DHT11_001=DHT11(pin=2)
    DHT11_001.client_id='DHT11_001'
    DHT11_001.pub_topic='/DHT11/{}/report-property'.format(DHT11_001.client_id)
    DHT11_001.client=create_client(DHT11_001)
    devices.append(DHT11_001)

    YL69_001=YL69()
    YL69_001.client_id='YL69_001'
    YL69_001.pub_topic='/YL69/{}/report-property'.format(YL69_001.client_id)
    YL69_001.client=create_client(YL69_001)
    devices.append(YL69_001)
        
    return devices
    # c1=create_client(DHT11_001)
    # c1.connect()
    # c2=create_client(YL69_001)
    # c2.connect()
def connect_all(devices):
    for device in devices:
        device.client.connect()

def disconnect_all(devices):
    for device in devices:
        device.client.disconnect()

async def pub(device,client):
    payload=await uasyncio.wait_for(device.get_data(),None)
    client.publish(device.pub_topic,payload)
    print('{} published to topic {}'.format(device.client_id,device.pub_topic))

async def main(devices):
    
    while True:
        # uasyncio.create_task(pub(DHT11_001,c1))
        # uasyncio.create_task(pub(YL69_001,c2))
        for device in devices:
            uasyncio.create_task(pub(device,device.client))
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
    
# if __name__=='__main__':
#     try:
#         devices=initialize()
#         connect_all(devices)
#         uasyncio.run(main(devices))
#     finally:
#         disconnect_all(devices)

