import json
import machine
import time
from dht import DHT22
import urequests
import ubinascii
from umqttsimple import MQTTClient
from env_variables import ENV_VARIABLES


# ------------------- SET UP MQTT BROKER -------------

# Set up MQTT_BROKER info to connect
CLIENT_ID = ubinascii.hexlify(machine.unique_id()) # To create an MQTT client, we need to get the PICOW unique ID
MQTT_BROKER = 'io.adafruit.com' # MQTT broker IP address or DNS  
PORT = ENV_VARIABLES['PORT']
ADAFRUIT_USERNAME = ENV_VARIABLES['ADAFRUIT_USERNAME']
ADAFRUIT_PASSWORD = ENV_VARIABLES['ADAFRUIT_PASSWORD']

# Set up Adafruit feed/group URI's
TOPIC_LED = b'CarolineA/feeds/temperature-and-humidity-and-airquality-and-led.led'
TOPIC_TEMP_HUMIDITY_AIRQUALITY_LED = b'CarolineA/groups/temperature-and-humidity-and-airquality-and-led'


# ---------------- SET UP OWN API ROUTES --------------

# api_url_temp = 'https://totus.serveo.net/api/temperature'
# api_url_humidity = 'https://totus.serveo.net/api/humidity'
# api_url_airquality = 'https://totus.serveo.net/api/airquality'


# ---------------- SET UP PICO W ----------------------

onboard_led = machine.Pin('LED', machine.Pin.OUT)
# Setup external LED as output
led_dht = machine.Pin(10, machine.Pin.OUT)
led_mq = machine.Pin(14, machine.Pin.OUT)

# Set up sensor pins
analog_mq135_pin = machine.ADC(28)
dht_pin = machine.Pin(22, machine.Pin.OUT)
mq135_pin = machine.Pin(21, machine.Pin.IN)

# Create sensor objects
dht22_sensor = DHT22(dht_pin)

# Publish MQTT messages after every set timeout
last_publish = time.time()  # last_publish variable will hold the last time a message was sent.
publish_interval = 5 #5 seconds

# Received messages from subscriptions will be delivered to this callback
def subscription_callback(topic, msg):
    print((topic, msg))
    if msg.decode() == 'on':
        onboard_led.value(1)
    else:
        onboard_led.value(0)

# if PicoW Failed to connect to MQTT broker. Reconnecting..
def reset():
    print('Resetting...')
    time.sleep(5)
    machine.reset()

print(f'Begin connection with MQTT Broker :: {MQTT_BROKER}')
mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
mqttClient.set_callback(subscription_callback) # whenever a new message comes (to picoW), print the topic and message (The call back function will run whenever a message is published on a topic that the PicoW is subscribed to.)
mqttClient.connect()
mqttClient.subscribe(TOPIC_LED)
print(f'Connected to MQTT  Broker :: {MQTT_BROKER}, waiting for callback function to be called!')

while True:
    print('Hello from Main.py')
    
    # DHT22 SENSOR MEASUREMENT
    dht22_sensor.measure()
    temp = dht22_sensor.temperature()
    humidity = dht22_sensor.humidity()

    time.sleep(5)

    if humidity > 80:
        led_dht.toggle()
    elif humidity > 70:
        led_dht.value(1)
    else:
        led_dht.value(0)


    print('Temperature: {}'.format(dht22_sensor.temperature()))
    print('Humidity: {}'.format(dht22_sensor.humidity()))

    # MQ-135 SENSOR MEASUREMENTS

    # Read the digital signal from the MQ-135 sensor
    digital_air_quality_value = mq135_pin.value()
    
    # Read the analog signal from the MQ-135 sensor
    air_quality_value = analog_mq135_pin.read_u16()

    if digital_air_quality_value == 0:
        led_mq.value(1)
    else:
        led_mq.value(0)
    
    print('Analog Air quality value: ', air_quality_value)
    print('Digital Air quality value: ', digital_air_quality_value)

    if digital_air_quality_value == 1:
        print('No, no gas detected.')
    else:
        print('Yes, gas detected!')

    # -------------- SENDING DATA TO ADAFRUIT VIA MQTT ----------------

    # Non-blocking wait for message
    mqttClient.check_msg()

    if (time.time() - last_publish) >= publish_interval:
        sensorData = {
            'feeds': {
                'Temperature': temp,
                'Humidity': humidity,
                'Airquality': digital_air_quality_value
            }
        }

        payload = json.dumps(sensorData)
        
        mqttClient.publish(TOPIC_TEMP_HUMIDITY_AIRQUALITY_LED, payload.encode())
        
        last_publish = time.time()
        print('Published!')

    # -------------- SENDING DATA VIA OWN BUILT DOTNET API ----------------

    # # Prepare the data payload
    # tempData = {
    #     'temperature': temp
    # }

    # humidityData = {
    #     'humidity': humidity
    # }

    # airqualityData = {
    #     'airquality': digital_air_quality_value
    # }


    # # Convert the data objects to JSON
    # tempDataJson = json.dumps(tempData)
    # humidityDataJson = json.dumps(humidityData)
    # airqualityDataJson = json.dumps(airqualityData)

    # headers = {'Content-Type': 'application/json'}

    # print('Json data:')
    # print(tempDataJson)
    # print(humidityDataJson)
    # print(airqualityDataJson)

    # # Send the data to API
    # urequests.post(api_url_temp, json=tempDataJson)


    # urequests.post(api_url_humidity, json=humidityDataJson)

    
    # urequests.post(api_url_airquality, json=airqualityDataJson)

    # -------------- SENDING DATA VIA ELK STACK ------------------

    # # Prepare data payloads
    # temp_payload = {
    #     "data_type": "temperature",
    #     "value": temp
    # }

    # humidity_payload = {
    #     "data_type": "humidity",
    #     "value": humidity
    # }

    # airquality_payload = {
    #     "data_type": "air_quality",
    #     "value": digital_air_quality_value
    # }

    # # Send HTTP POST requests to Logstash
    # temp_response = urequests.post(logstash_url, json=temp_payload)

    # # Check response status code
    # if temp_response.status_code == 200:
    #     print("Temp Data sent successfully")
    # else:
    #     print("Failed to send temp data. Status code:", temp_response.status_code)

    # temp_response.close()

    # # Send HTTP POST requests to Logstash
    # humidity_response = urequests.post(logstash_url, json=humidity_payload)

    # # Check response status code
    # if humidity_response.status_code == 200:
    #     print("Humidity Data sent successfully")
    # else:
    #     print("Failed to send humidity data. Status code:", humidity_response.status_code)

    # humidity_response.close()

    # # Send HTTP POST requests to Logstash
    # airquality_response = urequests.post(logstash_url, json=airquality_payload)

    # # Check response status code
    # if airquality_response.status_code == 200:
    #     print("Airquality Data sent successfully")
    # else:
    #     print("Failed to send airquality data. Status code:", airquality_response.status_code)

    # airquality_response.close()

