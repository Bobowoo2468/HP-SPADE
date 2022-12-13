#!/usr/bin/env python
import sys
import multiprocessing as mp
import globalparams as gp, globalfunctions as gf
import gui
import random
from time import sleep

#-----------------------IMPORT FROM USER DIRECTORY-----------------------#

sys.path.insert(0, gp.USER_DIRECTORY)
import params as user_p
import functions as user_f


#-----------------------PROCESS 1: LINUX PROCESS-----------------------#

def linux_f(q):
        
    with open(gp.LINUX_LOG_FILE_PATH, "a") as serial_dump:
        
        while True:
            
            while gp.LINUX.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.LINUX.readline()
                    decoded = received_line.decode('ascii') # DECODE CARRIAGE RETURN (/r) AND NEWLINE (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    
                    
                    #-----------ADD CORRESPONDING FUNCTION TO QUEUE-------------#
                    
                    for key in user_p.LINUX_KEYWORD_DICTIONARY.keys():
                        if key in str(received_line):
                            params_dict = {"key": key, "exec": str(user_p.LINUX_KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                            q.put(params_dict)

                            gf.console_log("LINUX KEY MATCH:" + key) # SHOW KEYWORD MATCH
                            
                    gf.file_log(serial_dump, decoded_str)
                    
                except Exception as e:
                    gf.console_log("LINUX SERIAL ERROR: " + str(e))
                    pass


#-----------------------PROCESS 2: RTOS PROCESS-----------------------#

def rtos_f(q):
    
    with open(gp.RTOS_LOG_FILE_PATH, "a") as serial_dump:
        
        #-----------CONTINUOUS LOOP TO DETECT KEYWORD MATCH-------------#
        
        while True:
                
            while gp.RTOS.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.RTOS.readline()
                    decoded = received_line.decode('ascii') # DECODE CARR RETURN (/r) AND NEWLINE (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    
                    
                    #-----------RANDOM ADD ASSERT TO ALL LINES OF RTOS OUTPUT-------------#
                    
                    if (random.random() > 0.9999):
                        received_line_test = str(received_line)+"asserted"
                    else:
                        received_line_test = str(received_line)
                    
                    
                    #-----------ADD CORRESPONDING FUNCTION TO QUEUE-------------#
                        
                    for key in user_p.KEYWORD_DICTIONARY.keys():
                        if key in str(received_line_test): # KEY DETECTION
                            params_dict = {"key": key, "exec": str(user_p.KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                            q.put(params_dict)
                            
                            gf.console_log("RTOS KEY MATCH:" + key) # SHOW KEYWORD MATCH
                    
                    gf.file_log(serial_dump, decoded_str)
                    
                except Exception as e:
                    gf.console_log("RTOS SERIAL ERROR: " + str(e))
                    pass


#-----------------------PROCESS 3: TRANSMIT PROCESS-----------------------#
                
def exec_f(q):
    
    while True:
    
        #-----------WHILE THERE ARE FUNCTIONS YET TO BE EXECUTED-------------#
        
        while q:
            params = q.get() # POP CORRESPONDING FUNCTION FROM QUEUE
            key = params["key"]
            func = params["exec"]
            
            #-----------EXECUTE FUNCTION WITH LOGGING-------------#
            
            gf.console_log("CALLING: {0} - KEY MATCHED: {1}".format(func, key))
            
            res = getattr(user_f, func)(key, params["dataline"]) # FUNCTION EXECUTION
            
            parsed_cmd = gf.parse_input_cmd(func, 0, gp.AUTO_PREPEND_INDICATOR)
            gf.simple_logger_append(user_p.FILE_NAMES["command_log"], parsed_cmd)
            
            gf.console_log("COMPLETED: {0} - KEY MATCHED: {1}".format(func, key))
            


if __name__ == '__main__':
    
    #-----------MULTIPROCESSING QUEUE----------------#
    
    keyword_queue = mp.Queue()
    
    #-----------CLEAR LOG FILES----------------#
    
    for file_name in user_p.FILE_NAMES.values():
        open(file_name, "w").close()

    #-----------START PROCESSES----------------#
    
    rtosp = mp.Process(target=rtos_f, args=(keyword_queue,))
    linuxp = mp.Process(target=linux_f, args=(keyword_queue,))
    execp = mp.Process(target=exec_f, args=(keyword_queue,))
    
    rtosp.start()
    linuxp.start()
    execp.start()
    
    gui.gui_f(keyword_queue)
    
    try:
        rtosp.join()
        linuxp.join()
        execp.join()
    except:
        exit()
        