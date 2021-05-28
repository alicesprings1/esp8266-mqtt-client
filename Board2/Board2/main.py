import sensors
import network

if __name__=='__main__':
    print('main.py running')
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        wlan.connect('wifi_name','wifi_password')
        print(wlan.isconnected())
    sensors.main_process()
