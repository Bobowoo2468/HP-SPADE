import globalfunctions as gf
import globalparams as gp
import os
from datetime import datetime
from time import sleep

from user import params as user_p

#-----------------------EXAMPLE FUNCTION CALLS-----------------------#
#
# RTOS TRANSMIT: gp.RTOS.write(gf.string_to_byte('udws "XXX"'))
# LINUX TRANSMIT: gp.LINUX.write(gf.string_to_byte('restart'))
# PRINT AND LOG CONSOLE: gf.console_log('XXX')
#
#-----------------------EXAMPLE FUNCTION CALLS-----------------------#


#-----------------------STRING PARSERS-----------------------#

def parse_data_from_dataline(dataline):
    return dataline.split(": ")[1]

#-----------------------HELPER FUNCTIONS-----------------------#


#-----------------------RESULT HANDLER FUNCTIONS-----------------------#

    
#-------------------------------------------------------------------TEST FUNCTIONS--------------------------------------------------------------------#

def empty_test(key, dataline):
    sleep(5)
    return

#------------PING WIRELESS CONFIG EVERY 10S, LOG NOISE AND SIGNAL STRENGTH----------#

def ping_wireless_config(key, dataline):
    gp.RTOS.write(gf.string_to_byte('udws "nca.get_wireless_config"'))
    signal_strength = parse_data_from_dataline(dataline)
    gf.timed_logger_append(user_p.FILE_NAMES["signal_strength"], dataline)
    gf.console_log("STRENGTH: " + dataline)
    sleep(10)
    return

def log_wireless_config_noise(key, dataline):
    noise = parse_data_from_dataline(dataline)
    gf.timed_logger_append(user_p.FILE_NAMES["noise"], dataline)
    gf.console_log("NOISE: " + dataline)
    return 

#------------PING WIRELESS SCAN EVERY 5S----------#

def ping_wireless_scan(key, dataline):
    gp.RTOS.write(gf.string_to_byte('udws "nca.get_wireless_scan"'))
    sleep(5)
    return

#------------RESTART SYSTEM CONTINUOUSLY UNTIL ASSERT APPEARS----------#

def restart(key, dataline):
    if user_p.assert_flag == 0:
        gf.timed_logger_append(user_p.FILE_NAMES["command_log"], 'udws "smgr_init.restart 0"')
        gp.RTOS.write(gf.string_to_byte('udws "smgr_init.restart 0"'))
        gf.console_log("RESTARTED")
        sleep(20)
    else:
        gf.console_log("STOP RESTARTING")
        sleep(3)
    return

def halt_restart(key, dataline):
    user_p.assert_flag = 1
    gf.console_log("ASSERT ASSERT ASSERT")
    return
    
#-----------------------INPUT FUNCTION-----------------------#

def user_input(key, dataline):
    if key == "RTOS":
        gp.RTOS.write(gf.string_to_byte(dataline))
    elif key == "LINUX":
        gp.LINUX.write(gf.string_to_byte(dataline))
    return