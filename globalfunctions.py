from time import sleep
import globalparams as gp

#-----------------------HELPER FUNCTIONS-----------------------#

# PACKAGE COMMAND TO BYTE_ENCODING (FOR SERIAL)
def string_to_byte(cmd_string):
    return str.encode(cmd_string + "\r")

#-----------------------TEST FUNCTIONS-----------------------#

def ping_wireless_config(key, dataline):
    gp.SER.write(string_to_byte('udws "nca.get_wireless_config"'))
    sleep(2)
    signal_strength = dataline.split(": ")[1]
    return signal_strength

def ping_wireless_scan(key, dataline):
    gp.SER.write(string_to_byte('udws "nca.get_wireless_scan"'))
    sleep(2)
    
def restart(key, dataline):
    gp.SER.write(string_to_byte('udws "smgr_init.restart 0"'))
    
def test_repeated_reboot(key, dataline):
    gp.SER.write(string_to_byte('udws "smgr_init.restart 0"'))
    