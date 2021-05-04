import machine
import time
import dht
import json
from simple import MQTTClient

config={
  'client_id':'DHT11_001',
  'user':'admin',
  'password':'admin',
  'server':'120.77.223.118',
  'port':1883,
  'pub_topic':'/DHT11/report-property'
}

def get_temp_hum(d):
    d.measure()
    return d.temperature(),d.humidity()

def main():
    global client
    client=MQTTClient(config['client_id'],config['server'],config['port'],config['user'],config['password'])
    client.connect()
    d=dht.DHT11(machine.Pin(2))
    print('Connected to %s, published to %s topic'%(config['server'],config['pub_topic']))
    while(True):
        temp,humid=get_temp_hum(d)
        payload={'temperature':temp,'humidity':humid}
        client.publish(config['pub_topic'],json.dumps(payload))
        time.sleep(5)

if __name__=='__main__':
    try:
        main()
    finally:
        client.disconnect()

