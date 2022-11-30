import globalparams as gp
import os
import multiprocessing as mp
from datetime import datetime

# from user import params as user_p
# from user import functions as user_f

#-----------------------STRING PARSERS-----------------------#

# PARSE INPUT COMMAND WITH DATETIME
def parse_input_cmd(string, cmd_no):
    current_time = get_current_time()
    parsed_input = "Command " + str(cmd_no) + ": "  + str(current_time) + " - " + string.rstrip().lstrip() + "\n"
    return parsed_input

def remove_whitespace(string):
    return "".join(string.rstrip().lstrip())

#-----------------------HELPER FUNCTIONS-----------------------#

def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

# PACKAGE COMMAND TO BYTE_ENCODING (FOR SERIAL)
def string_to_byte(cmd_string):
    return str.encode(cmd_string + "\r")

def write_to_file(file_ref, write_str):
    file_ref.write(write_str)
    file_ref.flush()
    os.fsync(file_ref.fileno())    
    return

def destroy_process_children():
    active = mp.active_children()
    for child in active:
        child.terminate()
    return

# RETURN LAST LINE FOUND IN LOG FILE - TO BE PRINTED IN GUI
def get_lastline(file_path):
    with open(file_path, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
                
        except OSError:
            f.seek(0)

        # UPDATE GUI LOGGER WITH LAST LINE IN FILE
        last_line = f.readline().decode()
        return last_line

def get_line_count(file_path):
    count = 0
    with open(file_path, 'rb') as fp:
        for count, line in enumerate(fp):
            pass
    return count;

#-----------------------RESULT HANDLER FUNCTIONS-----------------------#

def simple_logger_append(file_name, res):
    with open(file_name, "a") as file:
        write_to_file(file, res)
    return
    