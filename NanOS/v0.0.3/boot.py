#================================================================================================================================================
#                                                              imports

# This file is executed on every boot (including wake-boot from deepsleep)
# It includes the entire code for the nanofloat, all functions are defined here

# Importing sleep to allow for waiting
from time import sleep, sleep_ms

# Importing Piston Position
# Reference save_position function to see how the position is updated.
import piston_pos
position = piston_pos.position

# Impoting sys, it is used in the sys.exit() function within endFunc()
import sys

# Importing the WiFi config files, which store the network name, or SSID, and the password
import wlan_cfg

# Importing the i2c library for our pressure sensor
#import ms5837

# Importing the following from the esp32's operating system:
#       - Pin to control GPIOs
#       - I2C to control sensors operating over the i2c serial bus
from machine import Pin, I2C, ADC

# Importing WebREPL to interface wirelessly with the controller's WiFi Access Point 
import webrepl

# Importing network which will allow the controller to start up its own WiFi Access Point
import network 

# Starting up the WiFi Access Point. In this case, the network is set to AP_IF, putting it into access point mode.
# In other use cases, the network may be set to STA_IF which sets it as a default station which can connect to WiFi.
try:
    ap = network.WLAN(network.STA_IF)
    ap.config(beep)
    print("Startup in Station Mode")
except:
    print("---")
    print("WARNING: ROUTER CONNECTION FAILED: Initializing Access-Point Mode")
    print("---")
    try:
        ap = network.WLAN(network.AP_IF)
        ap.config(ssid = wlan_cfg.network_name, max_clients = 1)
        ap.active(True)
        print("Startup in Access-Point Mode Successful")
    except:
        print("Startup in Access-Point Mode Failed, USB Connection Required")

# Starting up WebREPL access, which sets the password for access and assigns the default IP address to the controller
# Reset the psasword to what you prefer by changing it in the webrepl_cfg.py file, default is "123"
webrepl.start()

# Defining the GPIOs (digital pin numbers do not always align with true GPIO numbers, check Seeed Studio XIAO ESP32C3 datasheet)
d1 = Pin(1, Pin.IN) #------------------ Encoder A phase
d2 = Pin(2, Pin.IN) #------------------ Encoder B phase
d3 = Pin(21, Pin.OUT) #---------------- UNUSED
d4 = Pin(22) #------------------------- I2C bus SDA
d5 = Pin(23) #------------------------- I2C bus SCL
d6 = Pin(16, Pin.IN, Pin.PULL_DOWN) #-- Limit Switch input pin
d7 = Pin(17, Pin.OUT) #---------------- Limit Switch Pullup pin (Enable/Disable limit switch)
d8 = Pin(19, Pin.OUT) #---------------- UNUSED
d9 = Pin(20, Pin.OUT) #---------------- Motor Input 1
d10 = Pin(18, Pin.OUT) #--------------- Motor Input 2

# Defining the encoder read pins
en_A = d1
en_B = d2

# Defining the pins for the I2C bus and creating the i2c object
sda = d4
scl = d5
i2c = I2C(scl=scl, sda=sda)

# Defining the Limit Switch Pins and setting the limit switch activator pin to be pulled high, or enabled.
lim_sw_state = d6
lim_sw_activate = d7
lim_sw_activate.value(1)

# Defining the Motor Input Pins
motor1 = d9
motor2 = d10

#================================================================================================================================================
#                                                           piston_out

def piston_out():
    motor1.value(1)
    motor2.value(0)

#================================================================================================================================================
#                                                           piston_in

def piston_in():
    motor1.value(0)
    motor2.value(1)

#================================================================================================================================================
#                                                           piston_stop

def piston_stop():
    motor1.value(0)
    motor2.value(0)

#================================================================================================================================================
#                                                           save_position

def save_position():
    
    global position
    
    with open("piston_pos.py", "w") as f:

        f.write('position = %d' % (position))
        
        f.close()
        
#================================================================================================================================================
#                                                           position_reset

def position_reset():
    
    global position
    
    position = 0
    
    save_position()

#================================================================================================================================================
#                                                           piston_move

# piston_move() requires three arguments: method, target, and units (optional, raw counts assumed).
#
# method: a string which decides whether the piston should move an arbitrary delta_x or if it should move to a specified position.
# |
# '--> accepts: "rel" or "relative"
#               "abs" or "absolute"
#
# target: a float representing either the relative distance the piston should move or the absolute position to which it should move.
# |
# '--> accepts: for relative values, either positive or negative floats for retraction and extension respectively
#               for absolute values, only positive floats
#
# units: a string which defines the units of the target argument. If left unspecified, raw counts are used. (WORK IN PROGRESS, CURRENTLY SUPPRESSED)
# |
# '--> accepts: "cm" (centimeters)
#               "mm" (millimeters)
#               "revs_o" (revolutions of output shaft)
#               "revs_i" (revolutions of input shaft)

# A-Channel previous state tracker initialization
a_prev = 0

delta = 0

# Encoder ISR to run as the handler for the interrupt and update position
def encoder_isr(pin):
    global delta, a_prev
    a = en_A.value()
    if a != a_prev:
        delta += 1

# Initializing interrupt to watch the encoder outputs
en_A.irq(trigger=Pin.IRQ_RISING, handler=encoder_isr)

target_pos = position

def piston_move(method, input):
    
    input *= 2000000000
    
    global target_pos, position, delta
    
    print("Starting Position:", position)
    
    if method in ("rel","relative"):
        
        method_check = True
        target_pos = position + input
        method = "rel"
        
    elif method in ("abs","absolute"):
        
        method_check = True
        target_pos = input
        method = "abs"
        
    else:
        
        method_check = False
        print("Error: first argument in piston_move()")
        print("|")
        print("'--> Please enter a valid argument for the 'method' parameter.")
        print("     'method' accepts the following arguments: 'rel' or 'relative', and 'abs' or 'absolute'")
    
    if method_check == True and method == "rel":
        
        if input < 0:
            
            delta = 0
            
            piston_in()
            
            while position > target_pos:
                
                position -= delta

            piston_stop()
            
            save_position()
        
        else:
            
            delta = 0
            
            piston_out()
            
            while position + delta < target_pos:
                
                position += delta

            piston_stop()
            
            save_position()
    
    elif method_check == True and method == "abs":
        
        if position < target_pos:
            
            delta = 0
            
            piston_out()
            
            while position < target_pos:
                
                position += delta
                
            piston_stop()
            
            save_position()
        
        else:
            
            delta = 0
            
            piston_in()
            
            while position > target_pos:
                
                position -= delta
                
            piston_stop()
            
            save_position()
    
    print("New Position:", position)

#================================================================================================================================================
#                                                              dive

def dive(sleep_time):
#    
#    piston_in(58)
#    sleep(sleep_time)
#    piston_out()
#    sleep(sleep_time)
    pass

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
            
#================================================================================================================================================
#                                                              encoder_test

def encoder_test(repetitions):
    
    for n in range(repetitions):
        
        print("Encoder A:", en_A.value(), "Encoder B:", en_B.value())
        print(delta)
        
        sleep(0.1)

#================================================================================================================================================
#                                                              motor_test
def motor_test():
    
    motor1.value(0)
    motor2.value(0)
    
    print("-------")
    print("Beginning Motor Test. Input either 1, -1, or 0 to run the motor forwards, backwards, or stop, respectively.")
    print("Input 'end' to conclude the test.")
    print("-------")
    
    while True:
    
        direction = input()
        
        if direction == "end":
            motor1.value(0)
            motor2.value(0)
            print("Motor Test Concluded")
            break
    
        elif direction != "1" and direction != "0" and direction != "-1":
            print("ERROR: Input either 1, -1, or 0 to run the motor forwards, backwards, or stop, respectively.")
    
        elif direction == "1":
            motor1.value(1)
            motor2.value(0)
            print("Running Motor Forwards...")
        
        elif direction == "-1":
            motor1.value(0)
            motor2.value(1)
            print("Running Motor Backwards...")
        
        elif direction == "0":
            motor1.value(0)
            motor2.value(0)
            print("Stopping Motor...")    

#================================================================================================================================================
#                                                          sensor_test

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
