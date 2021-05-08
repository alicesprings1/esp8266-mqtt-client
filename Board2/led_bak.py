from machine import Pin
from simple import MQTTClient

p5=Pin(5,Pin.OUT)
def sub_cb(topic,msg): 
    print('received message {} from topic {}'.format(msg,topic))
    p5.on()

def main():
    led=MQTTClient(client_id='LED_001',server='120.77.223.118',port=1883,user='admin',password='admin')
    led.set_callback(sub_cb)
    led.connect()
    led.subscribe('/led')
    print('subscribed to topic /led')
    try:
        while True:
            led.wait_msg()
    finally:
        led.disconnect()
        p5.off()   
if __name__=='__main__':
    main()
    # try:
    #     led=MQTTClient(client_id='LED_001',server='120.77.223.118',port=1883,user='admin',password='admin')
    #     led.set_callback(on)
    #     led.connect()
    #     led.subscribe(topic='/LED')
    # finally:
    #     led.disconnect()
    #     p5.off()

