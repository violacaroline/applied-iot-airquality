import machine
import time

onboard_led = machine.Pin('LED', machine.Pin.OUT)
analog_pin = machine.ADC(28)

while True:
    print('Hello from Main.py')
    onboard_led.toggle()
    sensor_value = analog_pin.read_u16()
    print('Sensor value: ', sensor_value)
    time.sleep(3)