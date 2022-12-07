#!/usr/bin/env python
import sys
import multiprocessing as mp
import globalparams as gp
import globalfunctions as gf
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
                    decoded = received_line.decode('ascii') # DECODE carriage return (/r) and newline (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    
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

def main_f(q):
    
    #-----------CONTINUOUS LOOP TO DETECT KEYWORD MATCH-------------#
    
    with open(gp.RTOS_LOG_FILE_PATH, "a") as serial_dump:
        
        while True:
                
            while gp.RTOS.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.RTOS.readline()
                    decoded = received_line.decode('ascii') # DECODE carriage return (/r) and newline (/n): PYTHON LEXICAL ANALYSIS
                    decoded_str = str(decoded)
                    
                    #-----------RANDOM ADD ASSERT TO ALL LINES OF RTOS OUTPUT-------------#
                    
                    if (random.random() > 0.9985):
                        received_line_test = str(received_line)+"asserted"
                    else:
                        received_line_test = str(received_line)
                        
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
                
def sub_f(q):
    
    while True:
    
        while q:
            params = q.get()
            key = params["key"]
            func = params["exec"]
            gf.console_log("CALLING: {0} - KEY MATCHED: {1}".format(func, key))
            
            res = getattr(user_f, func)(key, params["dataline"])

            gf.console_log("COMPLETED: {0} - KEY MATCHED: {1}".format(func, key))
            
              
if __name__ == '__main__':
    
    #-----------MULTIPROCESSING QUEUE----------------#
    
    keyword_queue = mp.Queue()
    
    #-----------CLEAR LOG FILES----------------#
    
    for file_name in user_p.FILE_NAMES.values():
        open(file_name, "w").close()

    #-----------START PROCESSES----------------#
    
    p = mp.Process(target=main_f, args=(keyword_queue,))
    linuxp = mp.Process(target=linux_f, args=(keyword_queue,))
    subp = mp.Process(target=sub_f, args=(keyword_queue,))
    
    p.start()
    linuxp.start()
    subp.start()
    
    gui.gui_f(keyword_queue)
    
    try:
        p.join()
        linuxp.join()
        subp.join()
    except:
        exit()
        