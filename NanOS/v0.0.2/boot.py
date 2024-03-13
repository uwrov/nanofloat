#================================================================================================================================================
#                                                              imports

# This file is executed on every boot (including wake-boot from deepsleep)
# It includes the entire code for the nanofloat, all functions are defined here

# Importing sleep to allow for waiting
from time import sleep

# Impoting sys, it is used in the sys.exit() function within endFunc()
import sys

import wlan_cfg

import os

# Importing Pin to control GPIOs
from machine import Pin, I2C, deepsleep, PWM

# Importing WebREPL to interface wirelessly with the controller's WiFi Access Point
import webrepl

# Importing network which will allow the controller to start up its own WiFi Access Point
import network

import random

# Starting up the WiFi Access Point. In this case, the network is set to AP_IF, putting it into access point mode.
# In other use cases, the network may be set to STA_IF which sets it as a default station which can connect to WiFi.
ap = network.WLAN(network.AP_IF)
ap.config(ssid = wlan_cfg.network_name, max_clients = 1)
ap.active(True)

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

version = "0.0.2"

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
    print("----                            NanOS Ver.",version,"                           ----")
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
        sleep(random.randint(20,150)*0.01)
        print('-------')
        for i in range(len(self.items)):
            print(str(f'{self.items[i]}'))
        print('-------')

items_root = [menu_item(1,'Control Parameters'), 
            menu_item(2,'Sensors'), 
            menu_item(3,'Data/Storage'), 
            menu_item(4,'Wireless'), 
            menu_item(5,'Float Info'),
            menu_item(6,'Exit config menu')]

menu_root = menu(items_root)

items1 = [menu_item(1,'Variable Buoyancy Drive'),
          menu_item(2,'Deployment Parameters'),
          menu_item(3,'Indicator Lights'), 
          menu_item(4,'Depth Control'), 
          menu_item(5,'Deep Sleep'),
          menu_item(6,'Misc Settings'),
          menu_item(7,'Return')]

menu1 = menu(items1)

items11 = [menu_item(1,'Acceleration Settings'),
           menu_item(2,'Calibrate Neutral Buoyancy'),
           menu_item(3,'Return')]

menu11 = menu(items11)

items12 = [menu_item(1,'Automatic Dive Settings'),
           menu_item(2,'Adjust Dive Speed'),
           menu_item(3,''),
           menu_item(4,'Return')]

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

items4 = [menu_item(1,'Configure WLAN'),
          menu_item(2,'Configure WebREPL'),
          menu_item(3,'Return')]

menu4 = menu(items4)

items41 = [menu_item(1,'Set Network Name (aka SSID)'),
          menu_item(2,'WLAN access point - On (Default)'),
          menu_item(3,'WLAN access point - Off'),
          menu_item(4,'Return')]

menu41 = menu(items41)

items42 = [menu_item(1,'Set WebREPL Password'),
           menu_item(2,'WebREPL - On (Default)'),
           menu_item(3,'WebREPL - Off'), 
           menu_item(4,'Return')]

menu42 = menu(items42)

items_final = [menu_item(1,'Return')]

menu_final = menu(items_final)

def placeholder_func():
    print("This functionality has not been developed yet. It is coming soon...")
    menu_final.show()

def wireless_menu():
    
    print("Changing default wireless settings is not recommended!")
    print("These settings can be useful for debugging and customization,")
    print("but tweaking them under normal operational conditions should not be necessary.")
    menu4.show()

def wifi_name_change():
    
    if os.dupterm(None):
        
        print("WARNING: You are connected to the NanoFloat wirelessly. Network name change is only supported via a wired connection.")
        print("")
        print("     In order for the network name to be changed, the access point must be deactivated, then reactivated.")
        print("     Unexpected behavior may occur if the access point is restarted during a wireless connection.")
        print("")
        print("Connect via USB and try again.")
        menu_final.show()

    else:
        while True:

            print("Enter the new network name. Type 'end' to quit.")

            new_ssid = input()

            if new_ssid == "end":
                break
            
            else:
                print("Confirm new network name:")

                new_ssid_confirm = input()
 
                if new_ssid == new_ssid_confirm:

                    ap.active(False)
                    ap.config(ssid = new_ssid)
                    ap.active(True)

                    print("SSID successfully changed to '"+new_ssid+"'.")
                    break

                else:
                    print("Names do not match. Please try again.")
                    print("-------")


def webrepl_password_change():

    webrepl_cfg_file = open("webrepl_cfg.py", "w")
    webrepl_cfg_file.write("# This file contains the WebREPL password. It is required for secure remote access of the nanofloat.")
    webrepl_cfg_file.write("PASS =",new_ssid)
    webrepl_cfg_file.close()

def webrepl_menu_start():
    
    webrepl.start()
    print("WebREPL Enabled. Connect to the NanoFloat's WiFi Access Point to communicate wirelessly.")
    print("Access Point IP address: 192.168.4.1:8266")
    menu_final.show()

def webrepl_menu_stop():
    
    while True:

        print("-------")
        print("CAUTION: Are you sure you want to disable WebREPL? This will prevent wireless connection to the microcontroller.")
        print("[Y/N]")
        print("-------")

        yes_no = input()

        if yes_no == "y" or yes_no == "Y":
            webrepl.stop()
            print("WebREPL Disabled.")
            menu_final.show()
            break

        elif yes_no == "n" or yes_no == "N":
            menu_final.show()
            break

def wlan_menu_start():

    network.WLAN(network.AP_IF).active(True)
    print("WLAN activated. Connect to ESP_00C179 for wireless communications.")
    print("Access Point IP address: 192.168.4.1:8266")
    menu_final.show()

def wlan_menu_stop():
    
    while True:

        print("-------")
        print("CAUTION: Are you sure you want to disable WLAN? This will prevent wireless connection to the microcontroller.")
        print("[Y/N]")
        print("-------")

        yes_no = input()

        if yes_no == "y" or yes_no == "Y":
            network.WLAN(network.AP_IF).active(True)
            print("WLAN Disabled.")
            menu_final.show()
            break

        elif yes_no == "n" or yes_no == "N":
            menu_final.show()
            break

def float_info():
    print("NanOS Ver.",version)
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
        '0400000000':[wireless_menu,items4],
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

        '0410000000':[menu41.show,items41],
        '0420000000':[menu42.show,items42],

        '0411000000':[wifi_name_change,'0'],
        '0412000000':[wlan_menu_start,'0'],
        '0413000000':[wlan_menu_stop,'0'],

        '0421000000':[placeholder_func,'0'],
        '0422000000':[webrepl_menu_start,'0'],
        '0423000000':[webrepl_menu_stop,'0'],

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
            level -= 1

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
