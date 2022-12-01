import globalfunctions as gf
import globalparams as gp
import os
from datetime import datetime
from time import sleep

from user import params as user_p

#-----------------------STRING PARSERS-----------------------#


#-----------------------HELPER FUNCTIONS-----------------------#


#-----------------------RESULT HANDLER FUNCTIONS-----------------------#

def simple_logger_append(file, res):
    with open(file, "a") as file:
        gf.write_to_file(file, res)
    return
    
#-----------------------TEST FUNCTIONS-----------------------#

def ping_wireless_config(key, dataline):
    gp.RTOS.write(gf.string_to_byte('udws "nca.get_wireless_config"'))
    signal_strength = dataline.split(": ")[1]
    print(signal_strength)
    sleep(5)
    #gf.simple_logger_append(user_p.FILE_NAMES["signal_strength"], signal_strength)
    return 

def ping_wireless_scan(key, dataline):
    gp.RTOS.write(gf.string_to_byte('udws "nca.get_wireless_scan"'))
    sleep(5)
    return
    
def restart(key, dataline):
    if "assert" in dataline:
        return
    gf.simple_logger_append(user_p.FILE_NAMES["command_log"], 'udws "smgr_init.restart 0"')
    gp.RTOS.write(gf.string_to_byte('udws "smgr_init.restart 0"'))
    print("RESTARTED")
    return
    
    