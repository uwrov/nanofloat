#================================================================================================================================================
#                                                              imports

# This file is executed on every boot (including wake-boot from deepsleep)
# It includes the entire code for the nanofloat, all functions are defined here

# Importing sleep to allow for waiting
from time import sleep

# Impoting sys, it is used in the sys.exit() function within endFunc()
import sys

# Importing Pin to control GPIOs
from machine import Pin

# Importing WebREPL to interface wirelessly with the controller's WiFi Access Point
import webrepl

# Importing network and urequests which will allow the controller to start up its own WiFi Access Point
import network
import urequests

import random

# Starting up the WiFi Access Point. In this case, the network is set to AP_IF, putting it into access point mode.
# In other use cases, the network may be set to STA_IF which sets it as a default station which can connect to WiFi.
network.WLAN(network.AP_IF).active(True)

# Starting up WebREPL access, which sets the password for access and assigns the default IP address to the controller
# THE PASSWORD IS "nanofloat"
webrepl.start()

# Defining the GPIOs
d1 = Pin(3, Pin.OUT)
d2 = Pin(4, Pin.OUT)
d3 = Pin(5, Pin.OUT)
d4 = Pin(6, Pin.OUT)
d5 = Pin(7, Pin.OUT)
d6 = Pin(21, Pin.OUT)
d7 = Pin(20, Pin.OUT)
d10 = Pin(10, Pin.OUT)

# Setting all GPIOs to pull low initially, ERASE IF NOT NEEDED
d1.value(0)
d2.value(0)
d3.value(0)
d4.value(0)
d5.value(0)
d6.value(0)
d7.value(0)
d10.value(0)

#================================================================================================================================================
#                                                              nanofloat
def nanofloat():
    
    print("--------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------")
    print("----                                                                        ----")
    print("----                                                                        ----")
    print("----      _   _          _   _  ____  ______ _      ____       _______      ----")
    print("----     | \ | |   /\   | \ | |/ __ \|  ____| |    / __ \   /\|__   __|     ----")
    print("----     |  \| |  /  \  |  \| | |  | | |__  | |   | |  | | /  \  | |        ----")
    print("----     | . ` | / /\ \ | . ` | |  | |  __| | |   | |  | |/ /\ \ | |        ----")
    print("----     | |\  |/ ____ \| |\  | |__| | |    | |___| |__| / ____ \| |        ----")
    print("----     |_| \_/_/    \_\_| \_|\____/|_|    |______\____/_/    \_\_|        ----")
    print("----                                                                        ----")
    print("----                                                                        ----")
    print("----                                                                        ----")
    print("----                                                                        ----")
    print("----                            NanOS Ver. 0.0.1                            ----")
    print("----                                                                        ----")
    print("----                  Underwater Remotely Operated Vehicles                 ----")
    print("----                                 at the                                 ----")
    print("----                        University of Washnigton                        ----")
    print("----                                                                        ----")
    print("--------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------")
    print("----                                                                        ----")
    print("----  Visit us at: https://uwrov.org/                                       ----")
    print("----  Github: https://github.com/uwrov/                                     ----")
    print("----  Contact: uwrov@uw.edu                                                 ----")
    print("----                                                                        ----")
    print("--------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------")
    sleep(0.2)
    print("")
    print("Connected successfully to 192.168.4.1:8266")
    print("")
    sleep(0.2)
    print("")
    print("Type 'help()' for MicroPython help.")
    print("")
    print("Type 'float_help()' for a list of float commands.")

#================================================================================================================================================
#                                                              floatHelp
def float_help():
    
    print("NanOS Ver. 0.0.1")
    print("")
    print("For detailed help and support, visit https://github.com/uwrov/ or contact us at uwrov@uw.edu")
    print("")
    print("Nanofloat commands:")
    print("   float_help()      -- Get a list of commands and other resources. It seems you know how to use this one!")
    print("   float_config()    -- Input setup parameters for deployment. Complete this process in advance before each deployment.")
    print("   dive()            -- Initiate a deployment. Make sure to complete dive_setup() before following through with this command.")
    print("   motor_test()      -- Simple test setup for the buoyancy engine. Only use for dry testing.")
    print("                        It also replaces the functionality of a dive sequence in this prototype version.")
    print("   end_func()        -- Can be used to exit the execution of a file, though the local 'end' function is mostly used.")

#================================================================================================================================================
#                                                              checkVE

# checkVE stands for Check Valid Entry. It is called during config menu navigation to check if the user input is valid

def checkVE(choice,choiceNum):

    for i in range(choiceNum):
        if choice == str(i+1):
            stop = True

#================================================================================================================================================
#                                                              endFunc
def end_func():
    print("Type 'end' again to confirm exit.")
    print("Otherwise, press the 'Enter' key to continue the dive sequence.")
        
    confirmEnd = input()
    
    if confirmEnd == 'end':
        sys.exit()

#================================================================================================================================================
#                                                              floatConfig
            
# This code chunk defines all the config menus and options
            
class menu_item:
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __str__(self):
        return f'{self.number}. {self.name}'
    
class menu:
    def __init__(self, items):
        self.items = items

    def show(self):
        sleep(random.randint(0,150)*0.01)
        print('-------')
        for i in range(len(self.items)):
            print(str(f'{self.items[i]}'))
        print('-------')

end_states_dict = {}

items_root = [menu_item(1,'Control Parameters'), 
            menu_item(2,'Sensors'), 
            menu_item(3,'Data/Storage'), 
            menu_item(4,'Wireless'), 
            menu_item(5,'Float Info'),
            menu_item(6,'Exit config menu')]

menu_root = menu(items_root)

items1 = [menu_item(1,'Parameter 1'), 
            menu_item(2, 'Parameter 2'), 
            menu_item(3,'Parameter 3'), 
            menu_item(4,'Parameter 4'), 
            menu_item(5,'Parameter 5'),
            menu_item(6,'Parameter 6'),
            menu_item(7,'Return')]

menu1 = menu(items1)

items11 = [menu_item(1,'Change Parameter 1'),
            menu_item(2,'Return')]

menu11 = menu(items11)

items12 = [menu_item(1,'Change Parameter 2'),
            menu_item(2,'Return')]

menu12 = menu(items12)

items13 = [menu_item(1,'Change Parameter 3'),
            menu_item(2,'Return')]

menu13 = menu(items13)

items14 = [menu_item(1,'Change Parameter 4'),
            menu_item(2,'Return')]

menu14 = menu(items14)

items15 = [menu_item(1,'Change Parameter 5'),
            menu_item(2,'Return')]

menu15 = menu(items15)

items16 = [menu_item(1,'Change Parameter 6'),
            menu_item(2,'Return')]

menu16 = menu(items16)

items2 = [menu_item(1,'Pressure'), 
            menu_item(2, 'Conductivity'), 
            menu_item(3,'Temperature'),
            menu_item(4,'Return')]

menu2 = menu(items2)

items21 = [menu_item(1,'Calibrate Pressure'),
           menu_item(2, 'Sensor Info'),
            menu_item(3,'Return')]

menu21 = menu(items21)

items22 = [menu_item(1,'Calibrate Conductivity'),
           menu_item(2, 'Sensor Info'),
            menu_item(3,'Return')]

menu22 = menu(items22)

items23 = [menu_item(1,'Calibrate Temperature'),
           menu_item(2, 'Sensor Info'),
            menu_item(3,'Return')]

menu23 = menu(items23)

items3 = [menu_item(1,'Erase stored data'), 
            menu_item(2, 'Access stored data'), 
            menu_item(3,'Return')]

menu3 = menu(items3)

items4 = [menu_item(1,'WebREPL - On'), 
            menu_item(2, 'WebREPL - Off'), 
            menu_item(3, 'WiFi access point - On'),
            menu_item(4, 'WiFi access point - Off'),
            menu_item(5, 'WiFi station - On'),
            menu_item(6, 'WiFi station - Off'),
            menu_item(7,'Return')]

menu4 = menu(items4)

items_final = [menu_item(1,'Return')]

menu_final = menu(items_final)

def placeholder_func():
    print("This functionality has not been developed yet. It is coming soon...")
    menu_final.show()

def float_info():
    print("NanOS Ver. 0.0.1")
    print("Gen. 1 NanoFloat hardware: Seeed Studio XIAO ESP32C3, flashed with MicroPython")
    print("Micropython v1.22.2 (2024-02-22)")
    print("Dives completed: 0") # IMPLEMENT LATER ------------- IMPLEMENT LATER ------------- IMPLEMENT LATER ------------- IMPLEMENT LATER
    print("Dives till next maintenance cycle: 0")#------------- IMPLEMENT LATER ------------- IMPLEMENT LATER ------------- IMPLEMENT LATER
    print("Float owner: Remotely Operated Vehicles team at the University of Washington")
    print("Contact uwrov@uw.edu for more information on your specific float.")
    menu_final.show()

def float_config():
    
   class menu_item:
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __str__(self):
        return f'{self.number}. {self.name}'
    
class menu:
    def __init__(self, items):
        self.items = items

    def show(self):
        print('-------')
        sleep(random.randint(20,150)*0.01)
        for i in range(len(self.items)):
            print(str(f'{self.items[i]}'))
        print('-------')

end_states_dict = {}

items_root = [menu_item(1,'Control Parameters'), 
            menu_item(2,'Sensors'), 
            menu_item(3,'Data/Storage'), 
            menu_item(4,'Wireless'), 
            menu_item(5,'Float Info'),
            menu_item(6,'Exit config menu')]

menu_root = menu(items_root)

items1 = [menu_item(1,'Parameter 1'), 
            menu_item(2, 'Parameter 2'), 
            menu_item(3,'Parameter 3'), 
            menu_item(4,'Parameter 4'), 
            menu_item(5,'Parameter 5'),
            menu_item(6,'Parameter 6'),
            menu_item(7,'Return')]

menu1 = menu(items1)

items11 = [menu_item(1,'Change Parameter 1'),
            menu_item(2,'Return')]

menu11 = menu(items11)

items12 = [menu_item(1,'Change Parameter 2'),
            menu_item(2,'Return')]

menu12 = menu(items12)

items13 = [menu_item(1,'Change Parameter 3'),
            menu_item(2,'Return')]

menu13 = menu(items13)

items14 = [menu_item(1,'Change Parameter 4'),
            menu_item(2,'Return')]

menu14 = menu(items14)

items15 = [menu_item(1,'Change Parameter 5'),
            menu_item(2,'Return')]

menu15 = menu(items15)

items16 = [menu_item(1,'Change Parameter 6'),
            menu_item(2,'Return')]

menu16 = menu(items16)

items2 = [menu_item(1,'Pressure'), 
            menu_item(2, 'Conductivity'), 
            menu_item(3,'Temperature'),
            menu_item(4,'Return')]

menu2 = menu(items2)

items21 = [menu_item(1,'Calibrate Pressure'),
           menu_item(2, 'Sensor Info'),
            menu_item(3,'Return')]

menu21 = menu(items21)

items22 = [menu_item(1,'Calibrate Conductivity'),
           menu_item(2, 'Sensor Info'),
            menu_item(3,'Return')]

menu22 = menu(items22)

items23 = [menu_item(1,'Calibrate Temperature'),
           menu_item(2, 'Sensor Info'),
            menu_item(3,'Return')]

menu23 = menu(items23)

items3 = [menu_item(1,'Erase stored data'), 
            menu_item(2, 'Access stored data'), 
            menu_item(3,'Return')]

menu3 = menu(items3)

items4 = [menu_item(1,'WebREPL - On'), 
            menu_item(2, 'WebREPL - Off'), 
            menu_item(3, 'WiFi access point - On'),
            menu_item(4, 'WiFi access point - Off'),
            menu_item(5, 'WiFi station - On'),
            menu_item(6, 'WiFi station - Off'),
            menu_item(7,'Return')]

menu4 = menu(items4)

items_final = [menu_item(1,'Return')]

menu_final = menu(items_final)

def placeholder_func():
    print("This functionality has not been developed yet. It is coming soon...")
    menu_final.show()

def float_info():
    print("NanOS Ver. 0.0.1")
    print("Gen. 1 NanoFloat hardware: Seeed Studio XIAO ESP32C3, flashed with MicroPython")
    print("Micropython v1.22.2 (2024-02-22)")
    print("Dives completed: 0") # IMPLEMENT LATER ------------- IMPLEMENT LATER ------------- IMPLEMENT LATER ------------- IMPLEMENT LATER
    print("Dives till next maintenance cycle: 0")#------------- IMPLEMENT LATER ------------- IMPLEMENT LATER ------------- IMPLEMENT LATER
    print("Float owner: Remotely Operated Vehicles team at the University of Washington")
    print("Contact uwrov@uw.edu for more information on your specific float.")
    menu_final.show()

def float_config():
    
    print('-------')
    print('NanoFloat Configuration Menu')
    print('Type "end" at any point to quit the config menu.')

    menu_dict = {

        '0000000000':[menu_root.show,items_root],

        '0100000000':[menu1.show,items1],
        '0200000000':[menu2.show,items2],
        '0300000000':[menu3.show,items3],
        '0400000000':[menu4.show,items4],
        '0500000000':[float_info,items_final],

        '0110000000':[menu11.show,items11],
        '0120000000':[menu12.show,items12],
        '0130000000':[menu13.show,items13],
        '0140000000':[menu14.show,items14],
        '0150000000':[menu15.show,items15],
        '0160000000':[menu16.show,items16],

        '0210000000':[menu21.show,items21],
        '0220000000':[menu22.show,items22],
        '0230000000':[menu23.show,items23],

        '0310000000':[placeholder_func,'0'],
        '0320000000':[placeholder_func,'0'],
        '0330000000':[placeholder_func,'0'],

        '0410000000':[placeholder_func,'0'],
        '0420000000':[placeholder_func,'0'],
        '0430000000':[placeholder_func,'0'],
        '0440000000':[placeholder_func,'0'],
        '0450000000':[placeholder_func,'0'],
        '0460000000':[placeholder_func,'0'],

        '0111000000':[placeholder_func,'0'],
        '0121000000':[placeholder_func,'0'],
        '0131000000':[placeholder_func,'0'],
        '0141000000':[placeholder_func,'0'],
        '0151000000':[placeholder_func,'0'],
        '0161000000':[placeholder_func,'0'],

        '0211000000':[placeholder_func,'0'],
        '0221000000':[placeholder_func,'0'],
        '0231000000':[placeholder_func,'0'],
    }

    path = [0,0,0,0,0,0,0,0,0,0]

    level = 0

    choice = 0

    while True:

        path_convert = ""

        for i in range(len(path)):
            path_convert += str(path[i])

        menu_dict[path_convert][0]()

        choice = input()

        valid = False

        for i in range(len(menu_dict[path_convert][1])):
            if choice == str(i+1):
                valid = True
                break
        
        if choice == 'end':
            end_func()

        if valid == True and choice == str(len(menu_dict[path_convert][1])):
            path[level] = 0
            level += -1

        elif valid == True:
            level += 1
            path[level] = choice

        if level == -1:
                sys.exit()
    
#================================================================================================================================================
#                                                              motorTest
def motor_test():
    
    d1.value(0)
    d2.value(0)
    
    print("-------")
    print("Beginning Motor Test. Input either 1, -1, or 0 to run the motor forwards, backwards, or stop, respectively.")
    print("Input 'end' to conclude the test.")
    print("-------")
    
    while True:
    
        direction = input()
    
        if direction == "end":
            d1.value(0)
            d2.value(0)
            print("Motor Test Concluded")
            break
    
        elif direction != "1" and direction != "0" and direction != "-1":
            print("ERROR: Input either 1, -1, or 0 to run the motor forwards, backwards, or stop, respectively.")
    
        elif direction == "1":
            d1.value(0)
            d2.value(1)
            print("Running Motor Forwards...")
        
        elif direction == "-1":
            d1.value(1)
            d2.value(0)
            print("Running Motor Backwards...")
        
        elif direction == "0":
            d1.value(0)
            d2.value(0)
            print("Stopping Motor...")    

#================================================================================================================================================
#                                                              dive
def dive():

    print("-------")
    print("Beginning dive sequence...")
    print("Type 'end' at any point to exit dive sequence.")
    print("-------")
    
    while True:
        
        while True:
            print("Enter the dive depth in meters:")

            diveDepth = input()

            if diveDepth == 'end':
                end_func()
            
            else:
                break
        
        while True:
            print("Confirm dive depth:")
            
            confirmDiveDepth = input()
            
            if confirmDiveDepth == 'end':
                end_func()
            
            else:
                break
        
        if diveDepth != confirmDiveDepth:
            print("ERROR: Depths do not match.")
            print("---")
            
        else:
            while True:
                
                while True:
                    print("Press 'Enter' to begin Dive 1.")
                    
                    diveStart = input()
                    
                    if diveStart == 'end':
                        end_func()
                    
                    else:
                        break
                
                if diveStart == "":
                    while True:
                        print("Press 'Enter' again to confirm dive, otherwise type 'cancel'.")
                        
                        confirmDiveStart = input()
                        
                        if confirmDiveStart == 'end':
                            end_func()
                        
                        else:
                            break
                    
                    if confirmDiveStart == "":
                        print("Beginning Dive 1, diving to " + diveDepth + " meters.")
                        print("Be prepared to re-establish wireless connection for Dive 2 initiation.")
                        break
                    
        if diveDepth == confirmDiveDepth:
            break
    
    motor_test()


