# applied-iot-airquality

This is a simple IoT project using the MQ-135 gas sensor module as well as the DHT22 temperature and humidity sensor to collect some interesting qualities of the surrounding air.

# Tutorial Report Template

**Please keep the total length of the tutorial below 25k characters.** You can include code that is linked to a repository. Keep the code snippets in the tutorial short.

## Tutorial on how to build a temperature and humidity sensor

Give a short and brief overview of what your project is about.
What needs to be included:

- [ ] Title
- [ ] Your name and student credentials (xx666x)
- [ ] Short project overview
- [ ] How much time it might take to do (approximation)

## Title: Humidity and Temperature Station

### Name & Student Credentials

Andrea Viola Caroline Åkesson

ca223pw

### Project Overview

**MAKE SURE RED LED LAMP IS IMPLEMENTED**

I built a web thing that measures the temperature and humidity of its surroundings, when humidity reaches over a beyond sweaty level a red LED lamp will turn on. You can also control the microcontrollers onboard LED via the MQTT brokers UI.

### Estimated Time to Complete Project

### Objective

Describe why you have chosen to build this specific device. What purpose does it serve? What do you want to do with the data, and what new insights do you think it will give?

#### Why did I choose this project?

**MAKE SURE RED LED LAMP IS IMPLEMENTED**

Simply because it seemed to be a good place for an introduction to IoT at a beginner friendly level and I could also extend it slightly with external LED lamps.

#### What purpose does it serve

It measures the temperature and humidity of my island home at Isla Mujeres, Mexico. Also, sending a warning through lighting a LED lamp as humidity rises.

#### What insights do you think it will give

How very, very hot the summer months here in the carribean really is. 

Jokes aside, purely data wise I had no idea that it was so much more humid here than Sweden, almost double at over 60% compared to some of the measurements done by fellow students back home.

Also it has given me insights into electrical circuits and components used for minor IoT projects, along with protocols and how parts interact with each other. From firmware being installed on Pico, to code uploaded on the Pico and then connectivity with wifi to get the data over to Adafruit.

### Material

Explain all material that is needed. All sensors, where you bought them and their specifications. Please also provide pictures of what you have bought and are using.


| IoT Thing | Specification    |  Bought via      | Price        |
| --------- | ---------------- | ---------------- | ---------------- |
| Raspberry Pi Pico W  | With headers, RP2040 processor  | Amazon   | 150kr |  
| Breadboard  | 830 points | Amazon   | 45kr |
| Female/Male Jumperwires | 30cm | Amazon | 30kr |       
| Male/Male Jumperwires | 30cm | Amazon  | Free  |  
| Resistors        | 10 pcs, 1W, 10kohm | Mercado Libre   | 30kr | 
| DHT22            | Humidity & Temperature sensor | Amazon  | 120kr |
| MQ-135           | Air Quality sensor detecting smoke, amoniac, alcohol etc. | Mercado Libre | 40kr |
| LED light        | 100 LED's, 5mm, 80mcd, 2.1v | Mercado Libre | 80kr | 


### Computer setup

How is the device programmed? Which IDE are you using? Describe all steps from flashing the firmware to installing plugins in your favorite editor and how flashing is done on MicroPython. The aim is that a beginner should be able to understand.

#### Chosen IDE

For this project I have chosen to use Visual Studio Code as my Integrated Development Environment. I have this IDE installed on my computer since before, but if you don't you can download it from here: https://code.visualstudio.com/download

#### Extensions

To interact with the Pico I will be using the extension "Pymakr" which you can find by searching for it under the "Extensions" tab on the left hand side of VSCode. This extensions simplifies the development and provides several tools and access to the REPL.

#### Flashing Pico

If the Pico W is new it will need the micropython firmware installed on it.

Download the UF2 file from here: https://micropython.org/download/rp2-pico-w/

You can then proceed to press the onboard bootsel button (placing the Pico W in download mode) while connecting the microcontroller to the computer. When the drive/file explorer (RPI-RP2) opens you can release the bootsel button and drag and drop the previously downloaded UF2 file onto the RPI-RP2, upon which the Pico will reboot and now run micropython

#### How the code is uploaded

To be able to actually run the code you write in VSCode you need to upload it to the Pico W first. You can do that by

#### Steps that you needed to do for your computer. Installation of Node.js, extra drivers, etc.

????????????????????

### Putting everything together

How is all the electronics connected? Describe all the wiring. Good if you can show a circuit diagram. Be specific on how to connect everything and what to think of in terms of resistors, current, and voltage. Is this only for a development setup, or could it be used in production?

- [ ] Circuit diagram (can be hand drawn)
- [ ] *Electrical calculations

### Platform

Describe your choice of platform. If you have tried different platforms, it can be good to provide a comparison.

Is your platform based on a local installation or a cloud? Do you plan to use a paid subscription or a free one? Describe the alternatives going forward if you want to scale your idea.

- [ ] Describe platform in terms of functionality
- [ ] *Explain and elaborate on what made you choose this platform


### The code

Import core functions of your code here, and don't forget to explain what you have done! Do not put too much code here. Focus on the core functionalities. Have you done a specific function that does a calculation, or are you using a clever function for sending data on two networks? Or, are you checking if the value is reasonable, etc.? Explain what you have done, including the setup of the network, wireless, libraries and all that is needed to understand.

#### Connecting to WIFI

To connect to the local wifi I created a seperate file and defined a method "connect" taking the SSID and the SSID-password as arguments, I could then call this method inside my main method.

Inside the function, it first checks if the device is already connected to a network. 
If not, it proceeds with the connection process.
It activates the Wi-Fi interface and attempts to connect to the specified network using the provided SSID and password.
While the device is not connected to the network, it repeatedly tries to connect with a one-second delay between attempts to give some time for the process before checking the connection status again.
Once the device is successfully connected, it prints a message confirming the connection and displays the network configuration details.

```
def connect(SSID, SSID_PASSWORD):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())

```

### Data flow / Connectivity

How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols and API information models, if any.

#### How often is the data sent?
#### Which wireless protocols did you use (WiFi, LoRa, etc ...)?
#### Which transport protocols were used (MQTT, webhook, etc ...)
#### Which information models were used (WoT TD, Fiware, etc...)
#### *Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.

### Presenting the data

Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?

#### Provide visual examples of how the dashboard looks. Pictures needed.
#### How often is data saved in the database.
#### *Explain your choice of database.
#### *Automation/triggers of the data.

### Finalizing the design

Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in another way, or even better? Some pictures are nice!

#### Show the final results of the project
#### Pictures
#### Video presentation of the project


