#!/usr/bin/env python
import sys
import multiprocessing as mp
import globalparams as gp, globalfunctions as gf
from gui import Gui
from wifiattenuator import WiFi_Attenuator

#-----------------------IMPORT FROM USER DIRECTORY-----------------------#

sys.path.insert(0, gp.USER_DIRECTORY)
import params as up
import functions as uf


#-----------------------PROCESS 1: LINUX PROCESS-----------------------#

def linux_f(q, e):
        
    with open(gp.LINUX_LOG_FILE_PATH, "a") as serial_dump:
        
        while True:            
            while gp.LINUX.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.LINUX.readline()
                    decoded = received_line.decode() # DECODE CARRIAGE RETURN (/r) AND NEWLINE (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    
                    gf.file_log(serial_dump, decoded_str)
                    
                    
                    #-----------IF STATUS IS START, PERFORM KEYWORD DETECTION AND ENQUEUE CORRESPONDING FUNCTION-------------#
                    
                    if e.is_set():
                        for key in up.LINUX_KEYWORD_DICTIONARY.keys():
                            if key in str(received_line):
                                params_dict = {"key": key, "exec": str(up.LINUX_KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                                q.put(params_dict)

                                gf.console_log("LINUX KEY MATCH," + key) # SHOW KEYWORD MATCH
                           
                           
                except Exception as ex:
                    gf.console_log("LINUX SERIAL ERROR," + str(ex))
                    pass


#-----------------------PROCESS 2: RTOS PROCESS-----------------------#

def rtos_f(q, e):
    with open(gp.RTOS_LOG_FILE_PATH, "a") as serial_dump:
        
        #-----------CONTINUOUS LOOP TO DETECT KEYWORD MATCH-------------#
        
        while True:
            
            while gp.RTOS.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.RTOS.readline()
                    decoded = received_line.decode() # DECODE CARR RETURN (/r) AND NEWLINE (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    gf.file_log(serial_dump, decoded_str)

                    
                    #-----------IF STATUS IS START, PERFORM KEYWORD DETECTION AND ENQUEUE CORRESPONDING FUNCTION-------------#

                    if e.is_set():
                        for key in up.KEYWORD_DICTIONARY.keys():
                            if key in str(received_line): # KEYWORD DETECTION
                                params_dict = {"key": key, "exec": str(up.KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                                q.put(params_dict)
                                
                                gf.console_log("RTOS KEY MATCH," + key) # SHOW KEYWORD MATCH
                    
        
                except Exception as ex:
                    gf.console_log("RTOS SERIAL ERROR," + str(ex))
                    pass


#-----------------------PROCESS 3: TRANSMIT PROCESS-----------------------#
                
def exec_f(q, e, wa):
    while True:
        
        #-----------WHILE THERE ARE FUNCTIONS YET TO BE EXECUTED-------------#
        
        while q:
            gf.console_log("QUEUE SIZE,{0}".format(q.qsize()))
            
            params = q.get() # POP CORRESPONDING FUNCTION FROM QUEUE            
            
            if params is None:
                e.clear()
                gf.console_log("AUTO DEBUG STOPPED ... AUTO DEBUG STOPPED ... AUTO DEBUG STOPPED ... AUTO DEBUG STOPPED")
                continue
            
            if params == "START":
                e.set()
                gf.console_log("AUTO DEBUG STARTED ... AUTO DEBUG STARTED ... AUTO DEBUG STARTED ... AUTO DEBUG STARTED")
                continue
                
            key = params["key"]
            func = params["exec"]
            
            if func == "user_input":
                gf.console_log("USER INPUT,{0},CHANNEL,{1}".format(func, key))
                
                getattr(gf, func)(key, params["dataline"]) # FUNCTION EXECUTION
            
                parsed_cmd = gf.parse_input_cmd(func, key)
                gf.timed_log(up.FILE_NAMES["command_log"], parsed_cmd)
                continue
            
            #-----------EXECUTE FUNCTION WITH LOGGING-------------#
            
            gf.console_log("CALLING,{0},KEY MATCHED,{1}".format(func, key))
            getattr(uf, func)(key, params["dataline"], wa) # FUNCTION EXECUTION
            
            parsed_cmd = gf.parse_input_cmd(func, gp.AUTO_PREPEND_INDICATOR)
            gf.timed_log(up.FILE_NAMES["command_log"], parsed_cmd)
            
            gf.console_log("COMPLETED,{0},KEY MATCHED,{1}".format(func, key))
            


if __name__ == '__main__':
    
    gf.gpio_init()
    
    #-----------MULTIPROCESSING VARIABLES----------------#
    
    keyword_queue = mp.Queue()
    start_event = mp.Event()
    start_event.set()
    
    #-----------CLEAR LOG FILES----------------#
    
    for file_name in up.CLEAR_FILE_NAMES.values():
        gf.init_logfiles(file_name) # CLEAR FILE AND APPEND HEADERS IF NECESSARY

        
    try:
        wifiattenuator = WiFi_Attenuator()
    
    except ValueError:
        wifiattenuator = False
        
    
    #-----------START PROCESSES----------------#
    
    rtosp = mp.Process(target=rtos_f, args=(keyword_queue,start_event,))
    linuxp = mp.Process(target=linux_f, args=(keyword_queue,start_event,))
    execp = mp.Process(target=exec_f, args=(keyword_queue,start_event,wifiattenuator,))
    
    rtosp.start()
    linuxp.start()
    execp.start()
    
    Gui(keyword_queue, wifiattenuator)
    
    try:
        rtosp.join()
        linuxp.join()
        execp.join()
    except:
        exit()
        