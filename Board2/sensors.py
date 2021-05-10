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
    return MQTTClient(device.client_id,device.server,device.port,device.user,device.password)

def led_initialize():
    global leds

    yellow=LED(pin=5)
    yellow.client_id='yellow'
    leds['yellow']=yellow

    green=LED(pin=4)
    green.client_id='green'
    leds['green']=green

    red=LED(pin=14)
    red.client_id='red'
    leds['red']=red

    for led in leds.values():
        led.sub_topic='/led/switch'
        led.client=create_client(led)
        led.client.set_callback(sub_cb)      
    
def rainsensor_initialize():
    device=RainSensor()
    device.client_id='RS_001'
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
        led.p.off()
        print('{} disconnected'.format(led.client_id))

async def led():
    global leds
    for led in leds.values():
        led.client.check_msg()

async def rainsensor(device):
    payload=await uasyncio.wait_for(device.get_data(),None)
    device.client.publish(device.pub_topic,payload)
    print('{} published to topic {}'.format(device.client_id,device.pub_topic))

async def led_loop():
    while True:
        uasyncio.create_task(led())
        await uasyncio.sleep_ms(5)

async def rainsensor_loop(device):
    while True:
        uasyncio.create_task(rainsensor(device))
        await uasyncio.sleep(5)

# async def main_loop(device):
#     while True:
#         uasyncio.create_task(led_loop())
#         uasyncio.create_task(rainsensor_main(device))
#         await uasyncio.sleep(5)

def main_process():
    try:
        led_initialize()
        led_connect_all()
        RS_001=rainsensor_initialize()
        RS_001.client.connect()
        uasyncio.run(rainsensor_loop(RS_001))
        uasyncio.run(led_loop())
        
        # led_loop()
        # uasyncio.gather(led_loop(),rainsensor_loop(RS_001))

    finally:
        led_disconnect_all()
        RS_001.client.disconnect()
        print('RS_001 disconnected')

if __name__=='__main__':
    main_process()



