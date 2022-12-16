#!/usr/bin/env python
import sys
import multiprocessing as mp
import globalparams as gp, globalfunctions as gf
import gui
import wifiattenuator as wa

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
                    decoded = received_line.decode('ascii') # DECODE CARRIAGE RETURN (/r) AND NEWLINE (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    
                    gf.file_log(serial_dump, decoded_str)
                    
                    
                    #-----------IF STATUS IS START, PERFORM KEYWORD DETECTION AND ENQUEUE CORRESPONDING FUNCTION-------------#
                    
                    if e.is_set():
                        for key in up.LINUX_KEYWORD_DICTIONARY.keys():
                            if key in str(received_line):
                                params_dict = {"key": key, "exec": str(up.LINUX_KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                                q.put(params_dict)

                                gf.console_log("LINUX KEY MATCH:" + key) # SHOW KEYWORD MATCH
                           
                           
                except Exception as ex:
                    gf.console_log("LINUX SERIAL ERROR: " + str(ex))
                    pass


#-----------------------PROCESS 2: RTOS PROCESS-----------------------#

def rtos_f(q, e):
    with open(gp.RTOS_LOG_FILE_PATH, "a") as serial_dump:
        
        #-----------CONTINUOUS LOOP TO DETECT KEYWORD MATCH-------------#
        
        while True:
            
            while gp.RTOS.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.RTOS.readline()
                    decoded = received_line.decode('ascii') # DECODE CARR RETURN (/r) AND NEWLINE (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    gf.file_log(serial_dump, decoded_str)

                    
                    #-----------IF STATUS IS START, PERFORM KEYWORD DETECTION AND ENQUEUE CORRESPONDING FUNCTION-------------#

                    if e.is_set():
                        for key in up.KEYWORD_DICTIONARY.keys():
                            if key in str(received_line): # KEYWORD DETECTION
                                params_dict = {"key": key, "exec": str(up.KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                                q.put(params_dict)
                                
                                gf.console_log("RTOS KEY MATCH:" + key) # SHOW KEYWORD MATCH
                    
        
                except Exception as ex:
                    gf.console_log("RTOS SERIAL ERROR: " + str(ex))
                    pass


#-----------------------PROCESS 3: TRANSMIT PROCESS-----------------------#
                
def exec_f(q, e):
    while True:
        
        #-----------WHILE THERE ARE FUNCTIONS YET TO BE EXECUTED-------------#
        
        while q:
            gf.console_log("QUEUE SIZE: {0}".format(q.qsize()))
            
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
            
            #-----------EXECUTE FUNCTION WITH LOGGING-------------#
            
            gf.console_log("CALLING: {0} - KEY MATCHED: {1}".format(func, key))
            
            getattr(uf, func)(key, params["dataline"]) # FUNCTION EXECUTION
            
            parsed_cmd = gf.parse_input_cmd(func, 0, gp.AUTO_PREPEND_INDICATOR)
            gf.simple_logger_append(up.FILE_NAMES["command_log"], parsed_cmd)
            
            gf.console_log("COMPLETED: {0} - KEY MATCHED: {1}".format(func, key))
            


if __name__ == '__main__':
    
    #-----------MULTIPROCESSING VARIABLES----------------#
    
    keyword_queue = mp.Queue()
    start_event = mp.Event()
    
    #-----------CLEAR LOG FILES----------------#
    
    for file_name in up.FILE_NAMES.values():
        open(file_name, "w").close()
    
    wifiattenuator = wa.WiFi_Attenuator()
    
    #-----------START PROCESSES----------------#
    
    rtosp = mp.Process(target=rtos_f, args=(keyword_queue,start_event,))
    linuxp = mp.Process(target=linux_f, args=(keyword_queue,start_event,))
    execp = mp.Process(target=exec_f, args=(keyword_queue,start_event,))
    
    rtosp.start()
    linuxp.start()
    execp.start()
    
    gui.gui_f(keyword_queue, wifiattenuator)
    
    try:
        rtosp.join()
        linuxp.join()
        execp.join()
    except:
        exit()
        