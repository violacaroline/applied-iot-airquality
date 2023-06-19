import machine
import time
from dht import DHT22


onboard_led = machine.Pin('LED', machine.Pin.OUT)
analog_pin = machine.ADC(28)
pin = machine.Pin(22, machine.Pin.OUT)
sensor = DHT22(pin)

while True:
    print('Hello from Main.py')
    time.sleep(3)
    
    onboard_led.toggle()


    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()

    print('Temperature: {}'.format(sensor.temperature()))
    print('Humidity: {}'.format(sensor.humidity()))

    air_quality_value = analog_pin.read_u16()
    print('Air quality value: ', air_quality_value)
