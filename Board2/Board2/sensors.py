from led import LED
from RainSensor import RainSensor
from simple import MQTTClient
import json
import uasyncio

leds={}

def sub_cb(topic,msg):
    global leds
    msg=json.loads(msg)
    print('received message {} from topic {}'.format(msg,topic))
    leds[msg['led']].shine(msg['status'])      

def create_client(device):
    return MQTTClient(device.client_id,device.server,device.port,device.user,device.password,keepalive=60)

def led_initialize():
    global leds

    yellow=LED('yellow',pin=5)
    leds['yellow']=yellow

    green=LED('green',pin=4)
    leds['green']=green

    red=LED('red',pin=14)
    leds['red']=red

    for led in leds.values():
        led.sub_topic='/led/switch'
        led.client=create_client(led)
        led.client.set_callback(sub_cb)      
    
def rainsensor_initialize():
    device=RainSensor('RS_001')
    device.pub_topic='/RS/{}/report-property'.format(device.client_id)
    device.client=create_client(device)
    return device

def led_connect_all():
    global leds
    for led in leds.values():
        led.client.connect()
        led.client.subscribe(led.sub_topic)
        print('{} subscribed to topic {}'.format(led.client_id,led.sub_topic))

def led_disconnect_all():
    global leds
    for led in leds.values():
        led.client.disconnect()
        led.shine('off')
        print('{} disconnected'.format(led.client_id))

def device_disconnect(device):
    device.client.disconnect()
    print('{} disconnected'.format(device.client_id))

async def led_loop(device):
    global leds
    try:
        while True:
            for led in leds.values():
                led.client.check_msg()
            await uasyncio.sleep_ms(5)
    finally:
        led_disconnect_all()
        device_disconnect(device)

async def rainsensor_loop(device):
    try:
        while True:
            payload=device.get_data()
            device.client.publish(device.pub_topic,payload)
            print('{} published to topic {}'.format(device.client_id,device.pub_topic))
            await uasyncio.sleep(5)
    finally:
        device_disconnect(device)
        led_disconnect_all()

def main_process():
    led_initialize()
    led_connect_all()
    RS_001=rainsensor_initialize()
    RS_001.client.connect()
    loop=uasyncio.get_event_loop()
    loop.create_task(led_loop(RS_001))
    loop.create_task(rainsensor_loop(RS_001))
    loop.run_forever()       

if __name__=='__main__':
    main_process()