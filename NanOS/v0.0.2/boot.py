#================================================================================================================================================
#                                                              imports

# This file is executed on every boot (including wake-boot from deepsleep)
# It includes the entire code for the nanofloat, all functions are defined here

# Importing sleep to allow for waiting
from time import sleep

# Impoting sys, it is used in the sys.exit() function within endFunc()
import sys

# Importing the WiFi config files, which store the network name, or SSID, and the password
import wlan_cfg

# Importing the i2c library for our pressure sensor
import ms5837

# Importing the following from the esp32's operating system:
#       - Pin to control GPIOs
#       - I2C to control sensors operating over the i2c serial bus
from machine import Pin, I2C

# Importing WebREPL to interface wirelessly with the controller's WiFi Access Point 
import webrepl

# Importing network which will allow the controller to start up its own WiFi Access Point
import network 

# Starting up the WiFi Access Point. In this case, the network is set to AP_IF, putting it into access point mode.
# In other use cases, the network may be set to STA_IF which sets it as a default station which can connect to WiFi.
ap = network.WLAN(network.AP_IF)
ap.config(ssid = wlan_cfg.network_name, max_clients = 1)
ap.active(True)

# Starting up WebREPL access, which sets the password for access and assigns the default IP address to the controller
# Reset the psasword to what you prefer by changing it in the webrepl_cfg.py file, default is "123"
webrepl.start()

# Defining the GPIOs (digital pin numbers do not always align with true GPIO numbers, check Seeed Studio XIAO ESP32C3 datasheet)

# Output pins:
d1 = Pin(3, Pin.OUT)
d2 = Pin(4, Pin.OUT)
d6 = Pin(21, Pin.OUT)
d7 = Pin(20, Pin.OUT)
d9 = Pin(9, Pin.OUT)
d10 = Pin(10, Pin.OUT)

# Input pin:
d3 = Pin(5, Pin.IN, Pin.PULL_DOWN)

# Setting d2 to pull high on boot since it feeds signal through the piston head limit switch, which is then read by input pin 3.
d2.value(1)
#================================================================================================================================================
#                                                           piston_out

def piston_out(runtime = 0):
    
    if runtime != 0:
        print("Confirm: override piston extension limiter? (Y/N)")
        conf = input()
        if conf in ["y","Y","yes","Yes"]:
            d10.value(1)
            d9.value(0)
            sleep(runtime)

    else:
        while d3.value() == 1:
            d10.value(1)
            d9.value(0)
    
    d10.value(0)

#================================================================================================================================================
#                                                           piston_in

def piston_in(runtime):
    d10.value(0)
    d9.value(1)
    sleep(runtime)
    d9.value(0)
    
#================================================================================================================================================
#                                                              motor_test
def motor_test():
    
    d9.value(0)
    d10.value(0)
    
    print("-------")
    print("Beginning Motor Test. Input either 1, -1, or 0 to run the motor forwards, backwards, or stop, respectively.")
    print("Input 'end' to conclude the test.")
    print("-------")
    
    while True:
    
        direction = input()
        
        if direction == "end":
            d10.value(0)
            d9.value(0)
            print("Motor Test Concluded")
            break
    
        elif direction != "1" and direction != "0" and direction != "-1":
            print("ERROR: Input either 1, -1, or 0 to run the motor forwards, backwards, or stop, respectively.")
    
        elif direction == "1":
            d10.value(1)
            d9.value(0)
            print("Running Motor Forwards...")
        
        elif direction == "-1":
            d10.value(0)
            d9.value(1)
            print("Running Motor Backwards...")
        
        elif direction == "0":
            d10.value(0)
            d9.value(0)
            print("Stopping Motor...")    

#================================================================================================================================================
#                                                          sensor_test

sda_pin = 6
scl_pin = 7

# Initialize the I2C bus
i2c = I2C(sda=Pin(sda_pin), scl=Pin(scl_pin))

# Setting all GPIOs to pull low initially, ERASE IF NOT NEEDED
d1.value(0)
d6.value(0)
d7.value(0)
d10.value(0)

# TO DO: Lubricate Actuator Cap, Fix UFL cable, fix strain relief, epoxy seal pressure sensor, 
# test battery voltage, make pusher piece, software test sensor, limit switch software, ballasting, 
# empty hull test, make spares or backups where possible, failure mode analysis


def sensor_test():
    print("-------")
    print("Beginning pressure sensor test. Connecting to the sensor...")
    sleep(0.2)
    print("...")
    sleep(0.1)
    print("...")
    
    
    
    pressure_sensor = ms5837.MS5837(ms5837.MODEL_30BA, 0)

    pressure_sensor.init()

    if pressure_sensor.init():
        print("Sensor connection established successfully.")
        sleep(0.1)
        print("Beginning sensor test. Type 'samp_c' to begin continuous sampling, or type 'samp_n:x' to sample x times.")
        print("Type 'end' to quit.")

        while True:

            test_input = input()

            if test_input == 'end':
                end_func()
            
            elif test_input[:-1] == 'samp_n:':
                for n in range(int(test_input[-1])):
                    print(pressure_sensor.pressure(ms5837.UNITS_kPa))
            
            elif test_input == 'samp_c':

                def constant_readout(run):

                    while run:
                        
                        print(pressure_sensor.pressure(ms5837.UNITS_kPa),end='\n',flush=True)
                        sleep(2)
                        print('\b',end='',flush=True)
                        for n in range(len(str(pressure_sensor.pressure(ms5837.UNITS_kPa)))):
                            print('\b',end='',flush=True)

                def interrupt():
                    user_input = input()
                    
                    if user_input == 'end':
                        pass


    else:
        print("Sensor connection failed.")

#================================================================================================================================================
#                                                              dive

def dive(sleep_time):
    
    piston_in(58)
    sleep(sleep_time)
    piston_out()
    sleep(sleep_time)

#================================================================================================================================================
#                                                              deploy

def deploy():

    print("-------")
    print("INITIATING DEPLOYMENT")
    print("Type 'confirm' to start the first dive. Any other input will cancel the deployment.")
    print("At any point that the NanoFloat is surfaced and wirelessly connected, pass the 'stop' command to prevent further automatic dives.")
    print("-------")
    
    conf_dive = input()

    if conf_dive != "confirm":
        sys.exit()
    
    print("-------")
    print("Diving...")
    print("Prepare to reconnect to the network upon dive completion.")
    print("-------")

    for n in range(6):
        try:
            dive(60) # CHANGE SLEEP TIME ACCORDINGLY
            
        except:
            print('Failed to dive. Entering Recovery mode.')
            piston_out()
            sys.exit()
