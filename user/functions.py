import os
import globalfunctions as gf, globalparams as gp
import gui

from datetime import datetime
from time import sleep
from user import params as up

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

    
#-------------------------------------------------------------------TEST FUNCTIONS--------------------------------------------------------------------#

def empty_test(key, dataline, wa):
    gf.console_log("EMPTY: " + dataline)
    sleep(5)
    return


#------------PING WIRELESS CONFIG EVERY 10S, LOG NOISE AND SIGNAL STRENGTH----------#

def ping_wireless_config(key, dataline, wa):
    gp.RTOS.write(gf.string_to_byte(up.GET_WIFI_CONFIG))
    signal_strength = parse_data_from_dataline(dataline)
    gf.timed_logger_append(up.FILE_NAMES["signal_strength"], "Signal Strength,{0}".format(signal_strength))
    sleep(10)
    return


def log_wireless_config_noise(key, dataline, wa):
    noise = parse_data_from_dataline(dataline)
    gf.timed_logger_append(up.FILE_NAMES["noise"], "Noise,{0}".format(noise))
    gf.console_log("NOISE: " + dataline)
    return 


#------------PING WIRELESS SCAN EVERY 5S----------#

def ping_wireless_scan(key, dataline, wa):
    gp.RTOS.write(gf.string_to_byte(up.GET_WIFI_SCAN))
    sleep(5)
    return


#------------RESTART SYSTEM CONTINUOUSLY UNTIL ASSERT APPEARS----------#

# def restart(key, dataline, wa):
#     if up.assert_flag == 0:
#         gp.LINUX.write(gf.string_to_byte('restart'))
#         gf.console_log("RESTARTED")
#         sleep(20)
#     else:
#         gf.console_log("STOP RESTARTING")
#         sleep(3)
#     return
# 
# 
# def halt_restart(key, dataline, wa):
#     up.assert_flag = 1
#     gf.console_log("ASSERT ASSERT ASSERT")
#     return


#------------MVP TEST 1: TEST CONTINUOUS RESTARTS----------#

shutdown_found = False
restart_success_found = False
restart_flag = False

def shutdown_success(key, dataline, wa):
    global shutdown_found
    if shutdown_found is True:
        gf.console_log("ALREADY TRUE BRO")
        return
    gf.console_log("SHUTDOWN SET TO TRUE BRO")
    shutdown_found = True
    return    

def restart_success(key, dataline, wa):
    global shutdown_found, restart_success_found, restart_flag
    
    if shutdown_found is False:
        restart_flag = False
        restart_success_found = False
        return
    
    if restart_success_found is True:
        gf.console_log("RESTART SUCCESS ALREADY TRUE")
    
    restart_success_found = True
    
    if shutdown_found and restart_success_found:
        restart_flag = True
        gf.console_log("RESTART SOONEST")
    return

def reset():
    global shutdown_found, restart_success_found, restart_flag
    shutdown_found = False
    restart_success_found = False
    restart_flag = False
    gf.console_log("RESETTED")
    return

def restart(key, dataline, wa):
    global restart_flag
    
    if restart_flag is False:
        gf.console_log("CONDITIONS TO RESTART NOT FULFILLED, EXITING")
        reset()
        return
    
    sleep(30)
    gp.LINUX.write(gf.string_to_byte('restart'))
    gf.console_log("RESTART SUCCESSFUL")
    up.restart_count += 1
    gf.timed_logger_append(up.FILE_NAMES["restart"], "RESTART COUNT, {0}\n".format(up.restart_count))
    reset()

    return


#------------MVP TEST 2: TEST SIGNAL ATTENUATION EFFICACY----------#

attenuation_asc = True
adjusted_attenuation = 0
ping_count = up.PING_NO

def set_attenuation_and_log(adjusted_attenuation, wa):
    wa.set_all_channels_attenuation(adjusted_attenuation)
    gf.timed_logger_append(up.FILE_NAMES["signal_strength"], "SET ATTENUATION,{0}\n".format(adjusted_attenuation))
    gf.timed_logger_append(up.FILE_NAMES["noise"], "SET ATTENUATION,{0}\n".format(adjusted_attenuation))
    
def reverse_attenuation(adj, asc):
        if asc is True and adj == up.MAX_ATTENUATION:
            return False
        
        if asc is False and adj == 0:
            return True
        
        return asc

def attenuation_control(wa):
    global adjusted_attenuation, ping_count, attenuation_asc
    
    if ping_count > 0:
        ping_count -= 1
    elif ping_count == 0:
        ping_count = up.PING_NO
        attenuation_asc = reverse_attenuation(adjusted_attenuation, attenuation_asc)
        
        if attenuation_asc is True:
            adjusted_attenuation += 1
        else:
            adjusted_attenuation -= 1
        set_attenuation_and_log(adjusted_attenuation, wa)
    return

def adjust_attenuation_and_ping_wifi(key, dataline, wa):
    if wa is False:
        return
    
    attenuation_control(wa)
    gp.RTOS.write(gf.string_to_byte(up.GET_WIFI_CONFIG))
    signal_strength = parse_data_from_dataline(dataline)
    gf.timed_logger_append(up.FILE_NAMES["signal_strength"], "Signal Strength,{0}".format(signal_strength))
    gf.console_log("STRENGTH: " + dataline)
    sleep(1)
    return


#-----------------------INPUT FUNCTION-----------------------#

def user_input(key, dataline, wa):
    if key == "RTOS":
        gp.RTOS.write(gf.string_to_byte(dataline))
    elif key == "LINUX":
        gp.LINUX.write(gf.string_to_byte(dataline))
    return