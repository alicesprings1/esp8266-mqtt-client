import time
import json
import uasyncio
from YL69 import YL69
from DHT11 import DHT11
from simple import MQTTClient

def create_client(device):
    client=MQTTClient(device.client_id,device.server,device.port,device.user,device.password)
    return client

DHT11_001=DHT11(pin=2)
DHT11_001.client_id='DHT11_001'
DHT11_001.pub_topic='/DHT11/{}/report-property'.format(DHT11_001.client_id)
YL69_001=YL69()
YL69_001.client_id='YL69_001'
YL69_001.pub_topic='/YL69/{}/report-property'.format(YL69_001.client_id)

c1=create_client(DHT11_001)
c1.connect()
c2=create_client(YL69_001)
c2.connect()

async def pub(device,client):
    payload=await uasyncio.wait_for(device.get_data(),None)
    client.publish(device.pub_topic,payload)
    print('{} published to topic {}'.format(device.client_id,device.pub_topic))

async def main():
    # print('main开始')
    
    # print('main结束')

    # await uasyncio.sleep(5)
    # done=await uasyncio.gather(DHT11_001.get_data(),YL69_001.get_data())
    # print(done)
    while True:
         await uasyncio.gather(pub(DHT11_001,c1),pub(YL69_001,c2)) 

uasyncio.run(main())