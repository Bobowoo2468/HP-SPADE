import os
import globalfunctions as gf, globalparams as gp

from datetime import datetime
from time import sleep
from user import params as up

#-----------------------ALL EXAMPLE FUNCTION CALLS-----------------------#
#
# RTOS TRANSMIT: [gf.rtos_write('XXX')]
# LINUX TRANSMIT: [gf.linux_write('XXX')]
# PRINT AND LOG CONSOLE: [gf.console_log('XXX')]
#
# PARSE DATA FROM LINE: [parse_data_from_dataline('')]                                   - RETURNS DATA IF DATA IS IN FORMAT, ABC: data
# PAUSE/DELAY: [sleep(x)]                                                                - WHERE x IS INTEGER, PAUSE IN NUMBER OF SECONDS
#
# TIMED APPEND TO LOGGER: [gf.timed_log(file_name, string_to_append)]                    - WRITES TO LOG FILE WITH TIMESTAMP. ARG 1: relative path and name of file, ARG 2: string to be logged
# UNTIMED APPEND TO LOGGER (NO NEW LINE): [gf.simple_log(file_name, string_to_append)]   - WRITES TO LOG FILE WITHOUT TIMESTAMP OR NEWLINE
#
# GET CURRENT TIME: gf.get_current_time()
# APPEND TIMESTAMP: gf.append_time(string), gf.append_time_wo_newline(string)



#-----------------------STRING PARSERS-----------------------#

def parse_data_from_dataline(dataline):
    return dataline.split(": ")[1]

    
#-------------------------------------------------------------------TEST FUNCTIONS--------------------------------------------------------------------#

def empty_test(key, dataline, wa):
    gf.console_log("EMPTY," + dataline)
    sleep(5)
    return


#------------PING WIRELESS CONFIG EVERY 10S, LOG NOISE AND SIGNAL STRENGTH----------#

def ping_wireless_config(key, dataline, wa):
    gf.rtos_write(up.GET_WIFI_CONFIG)
    data = parse_data_from_dataline(dataline)
    gf.timed_log(up.FILE_NAMES["signal_strength"], "{0}".format(data))
    sleep(10)
    return


def log_wireless_config_noise(key, dataline, wa):
    data = parse_data_from_dataline(dataline)
    gf.timed_log(up.FILE_NAMES["noise"], "{0}".format(data))
    gf.console_log("NOISE," + dataline)
    return 


#------------PING WIRELESS SCAN EVERY 5S----------#

def ping_wireless_scan(key, dataline, wa):
    gf.rtos_write(up.GET_WIFI_SCAN)
    sleep(5)
    return


#------------RESTART SYSTEM CONTINUOUSLY UNTIL ASSERT APPEARS----------#

# def restart(key, dataline, wa):
#     if up.assert_flag == 0:
#         gf.linux_write('restart')
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

# PROGRAM DESCRIPTION: ON KEYWORD MATCH OF "Shutdown" AND "/dev/btusb0", INITIATE RESTART
# IF EITHER KEY NOT MATCHED, DO NOT RESTART AND FLAG OUT ERROR

# INITIAL STATE OF FLAGS - ALL SET TO FALSE
shutdown_found = False
restart_success_found = False
restart_flag = False

# SET SHUTDOWN FLAG 
def shutdown_success(key, dataline, wa):
    global shutdown_found
    if shutdown_found is True:
        gf.console_log("ALREADY MATCHED")
        return
    shutdown_found = True
    return    

# SET RESTART SUCCESS FLAG 
def restart_success(key, dataline, wa):
    global shutdown_found, restart_success_found, restart_flag
    
    # EARLY EXIT IF SHUTDOWN KEY NOT MATCHED
    if shutdown_found is False:
        restart_flag = False
        restart_success_found = False
        gf.console_log("SHUTDOWN NOT MATCHED")
        return
    
    if restart_success_found is True:
        gf.console_log("ALREADY MATCHED")
    
    # KEYWORDS MATCHED - PERFORM RESTART
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
    return


def restart(key, dataline, wa):
    global restart_flag
    
    # LOG ERRORS DETECTED IN SERIAL DEBUG
    if restart_flag is False:
        gf.console_log("CONDITIONS TO RESTART NOT FULFILLED, EXITING")
        reset()
        return
    
    sleep(30)
    gf.linux_write('restart') # TRANSMIT 'restart' OVER LINUX CHANNEL
    gf.console_log("RESTART SUCCESSFUL")
    
    # INCREMENT AND LOG THE NUMBER OF RESTARTS DONE SUCCESSFULLY
    up.restart_count += 1 
    gf.timed_log(up.FILE_NAMES["restart"], "COUNT,{0}".format(up.restart_count))
    reset()
    return


#------------MVP TEST 2: TEST SIGNAL ATTENUATION EFFICACY----------#

attenuation_asc = True
adjusted_attenuation = 0
ping_count = up.PING_NO
iperf_connection = False

# SET UP IPERF CONNECTION BY TRANSMIT 'iperf3 -s' VIA LINUX CHANNEL
def set_iperf_connection():
    global iperf_connection
    
    # SET UP CONNECTION IF IPERF YET TO SET UP
    if iperf_connection is False:
        gf.linux_write("iperf3 -s")
        gf.console_log("IPERF CONN START")
        iperf_connection = True
    
    elif iperf_connection is True:
        gf.console_log("IPERF CONN ACTIVE")
    
    return

# SET ATTENUATION OF CHANNELS (1, 2, 3) TO adjusted_attenuation 
def set_attenuation_and_log(adjusted_attenuation, wa):
    wa.set_all_channels_attenuation(adjusted_attenuation)
    gf.timed_log(up.FILE_NAMES["signal_strength"], "SET ATTENUATION,{0}".format(adjusted_attenuation))
    gf.timed_log(up.FILE_NAMES["noise"], "SET ATTENUATION,{0}".format(adjusted_attenuation))
    gf.timed_log(up.FILE_NAMES["signal_strength"], "SET ATTENUATION,{0}".format(adjusted_attenuation))
    
    
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
    set_iperf_connection()
    attenuation_control(wa)
    gf.rtos_write(up.GET_WIFI_CONFIG)
    signal_strength = parse_data_from_dataline(dataline)
    gf.timed_log(up.FILE_NAMES["signal_strength"], "{0}".format(signal_strength))
    gf.console_log("SIGNAL STRENGTH," + dataline)
    sleep(1)
    return


def log_throughput(key, dataline, wa):
    if wa is False:
        return
    transfer = dataline[25:36]
    bandwidth = dataline[38:52]
    gf.timed_log(up.FILE_NAMES["throughput"], "{0},{1}".format(transfer, bandwidth))
    gf.console_log("THROUGHPUT," + dataline[25:])
    return 


#-----------------------INPUT FUNCTION-----------------------#

def user_input(key, dataline, wa):
    if key == "RTOS":
        gf.rtos_write(dataline)
    elif key == "LINUX":
        gf.linux_write(dataline)
    return