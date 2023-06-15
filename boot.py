import network, time
from env_variables import ENV_VARIABLES 

def connect(SSID, SSID_PASSWORD):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            time.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())

connect(ENV_VARIABLES['SSID'], ENV_VARIABLES['SSID_PASSWORD'])