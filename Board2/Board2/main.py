import sensors
import network

if __name__=='__main__':
    print('main.py running')
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        wlan.connect('Alice','HYXdlh666')
        print(wlan.isconnected())
    sensors.main_process()