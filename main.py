#!/usr/bin/env python
import sys
import multiprocessing as mp
import globalparams as gp
import globalfunctions as gf
import gui

#-----------------------IMPORT FROM USER DIRECTORY-----------------------#

sys.path.insert(0, gp.USER_DIRECTORY)
import params as user_p
import functions as user_f

def linux_f(keyword_queue):
    with open(gp.LINUX_LOG_FILE_PATH, "a") as serial_dump:
        
        while True:
            
            while gp.SER.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.LINUX.readline()
                    decoded = received_line.decode('ascii') # decode data to detect carriage return (/r) and newline (/n): see python lexical analysis
                    decoded_str = str(decoded)
                    
                    gf.write_to_file(serial_dump, decoded_str)
                except:
                    print("DECODE ERROR")
                    pass

def main_f(keyword_queue):
    
    #-----------ARTIFICIAL SERIAL WRITE-------------#
    
#     command = 'udws XXX'
#     gp.SER.write(gf.string_to_byte(command))

    #-----------CONTINUOUS LOOP TO DETECT KEYWORD MATCH-------------#
    
    with open(gp.SERIAL_LOG_FILE_PATH, "a") as serial_dump:
        
        while True:
            
            while gp.SER.inWaiting(): # IF DATA EXISTS IN BUFFER
                try:
                    received_line = gp.SER.readline()
                    decoded = received_line.decode('ascii') # decode data to detect carriage return (/r) and newline (/n): see python lexical analysis
                    decoded_str = str(decoded)
                    
                    for key in user_p.KEYWORD_DICTIONARY.keys():
                        
                        if key in str(received_line): # KEY DETECTION
                            params_dict = {"key": key, "exec": str(user_p.KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                            keyword_queue.put(params_dict)
                    
                    gf.write_to_file(serial_dump, decoded_str)
                except:
                    pass

def sub_f(keyword_queue):
    
    while True:
    
        while keyword_queue:
            params = keyword_queue.get()
            key = params["key"]
            res = getattr(user_f, params["exec"])(key, params["dataline"])
            
              
if __name__ == '__main__':
    
    #-----------MULTIPROCESSING VARIABLES----------------#
    
    keyword_queue = mp.Queue()
    
    #-----------CLEAR LOG FILES----------------#
    
    for file_name in user_p.FILE_NAMES.values():
        open(file_name, "w").close()

    #-----------START PROCESSES----------------#
    
    p = mp.Process(target=main_f, args=(keyword_queue,))
    p.start()
    
    subp = mp.Process(target=sub_f, args=(keyword_queue,))
    subp.start()
    
    linuxp = mp.Process(target=linux_f, args=(keyword_queue,))
    linuxp.start()
    
    gui.gui_f()
        