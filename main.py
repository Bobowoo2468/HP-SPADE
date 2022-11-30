#!/usr/bin/env python
import sys
import serial
import multiprocessing as mp
import globalparams as gp
import globalfunctions as gf
import gui
import os
import ctypes
import atexit

from time import sleep
    

def main_f(keyword_queue):
    
    #-----------ARTIFICIAL SERIAL WRITE-------------#

#     gp.SER.write(gf.string_to_byte('udws "nca.get_wireless_config"'))

    #-----------CONTINUOUS LOOP TO DETECT KEYWORD MATCH-------------#
    
    with open(gp.WRITE_FILE_NAME, "a") as serial_dump:
        
        while True:
            
            while gp.SER.inWaiting(): # IF DATA EXISTS IN BUFFER
                received_line = gp.SER.readline()
                decoded = received_line.decode('ascii') # decode data to detect carriage return (/r) and newline (/n): see python lexical analysis
                decoded_str = str(decoded)
                
                for key in gp.KEYWORD_DICTIONARY.keys():
                    
                    if key in str(received_line): # KEY DETECTION
                        params_dict = {"key": key, "exec": str(gp.KEYWORD_DICTIONARY[key]), "dataline": decoded_str}
                        keyword_queue.put(params_dict)
                
                serial_dump.write(decoded_str)
                serial_dump.flush()
                os.fsync(serial_dump.fileno())
                

def sub_f(keyword_queue):
    
    with open(gp.SIGNAL_STRENGTH_FILE_NAME, "a") as signal_strength:
        
        while True:
            
            while keyword_queue:
                params = keyword_queue.get()
                key = params["key"]
                rtn = getattr(gf, params["exec"])(key, params["dataline"])
                
                if key == "signalStrength" or key == "noise":
                    signal_strength.write(rtn)
                    signal_strength.flush()
                    os.fsync(signal_strength.fileno())
            

def exit_handler(main_process, sub_process):
    main_process.join()
    sub_process.join()
    main_process.terminate()
    sub_process.terminate()
    sys.exit(0)
    
              
if __name__ == '__main__':
    
    #-----------MULTIPROCESSING VARIABLES----------------#
    
    keyword_queue = mp.Queue()
    
    #-----------CLEAR LOG FILES----------------#
    
    open(gp.SIGNAL_STRENGTH_FILE_NAME, "w").close()
    open(gp.WRITE_FILE_NAME, "w").close()

    #-----------START PROCESSES----------------#
    
    p = mp.Process(target=main_f, args=(keyword_queue,))
    p.start()
    
    subp = mp.Process(target=sub_f, args=(keyword_queue,))
    subp.start()
    
    gui.gui_f()

    
