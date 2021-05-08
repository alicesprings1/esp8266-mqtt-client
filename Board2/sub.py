from led import LED
from simple import MQTTClient
import json


leds=[]

def sub_cb(topic,msg):
    msg=json.loads(msg)
    print('received message {} from topic {}'.format(msg,topic))
    leds[msg['led']].shine(msg['status'])      

def create_client(device):
    return MQTTClient(device.client_id,device.server,device.port,device.user,device.password)

def led_initialize():
    global leds

    yellow=LED(pin=5)
    yellow.client_id='yellow'
    leds.append(yellow)

    green=LED(pin=4)
    green.client_id='green'
    leds.append(green)

    red=LED(pin=14)
    red.client_id='red'
    leds.append(red)

    for led in leds:
        led.sub_topic='/led/{}/switch'.format(led.client_id)
        led.client=create_client(led)
        led.client.set_callback(sub_cb)
    

def led_connect_all():
    global leds
    for led in leds:
        led.client.connect()
        led.client.subscribe(led.sub_topic)
        print('{} subscribed to topic {}'.format(led.client_id,led.sub_topic))

def led_disconnect_all():
    global leds
    for led in leds:
        led.client.disconnect()
        led.p.off()

def main():
    global leds
    while True:
        for led in leds:
            led.check_msg()

def led_wait():
    try:
        led_initialize()
        led_connect_all()
        main()
    finally:
        led_disconnect_all()

if __name__=='__main__':
    led_wait()