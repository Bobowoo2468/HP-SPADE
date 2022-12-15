import os
import multiprocessing as mp
from datetime import datetime
import globalparams as gp


#-----------------------STRING PARSERS-----------------------#

# PARSE INPUT COMMAND WITH DATETIME
def parse_input_cmd(string, cmd_no, prepend):
    current_time = get_current_time()
    if cmd_no == 0:
        cmd_no = ""
    parsed_input = "{0}: Command {1}: {2} - {3}\n".format(prepend, cmd_no, current_time, string.rstrip().lstrip())
    return parsed_input


#--------------------------------HELPER FUNCTIONS--------------------------------#


#-----------------STRING PROCESSING FUNCTIONS------------------#

def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def append_time(write_str):
    return "{0}: {1}\n".format(get_current_time(), write_str)


def append_time_wo_newline(write_str):
    return "{0}: {1}".format(get_current_time(), write_str)


def remove_whitespace(string):
    return "".join(string.rstrip().lstrip())


# PACKAGE COMMAND TO BYTE_ENCODING (FOR SERIAL)
def string_to_byte(cmd_string):
    return str.encode(cmd_string + "\r")


#-----------------FILEWRITER FUNCTIONS------------------#
    
def file_write(file_ref, write_str):
    file_ref.write(write_str)
    file_ref.flush()
    os.fsync(file_ref.fileno())    
    return


def file_log(file_ref, write_str):
    timed_str = append_time_wo_newline(write_str)
    file_ref.write(timed_str)
    file_ref.flush()
    os.fsync(file_ref.fileno()) 


#-----------------FILEREADER FUNCTIONS------------------#

def get_line_count(file_path):
    count = -1
    with open(file_path, 'rb') as fp:
        for count, line in enumerate(fp):
            pass
    return count 


def get_last_Nlines(file_path, N):
    pos = N + 1
    lines = []
    with open(file_path) as f:
        while len(lines) <= N:
            try:
                f.seek(-pos, os.SEEK_END)
            except IOError:
                f.seek(0)
                break
            finally:
                lines = list(f)
            pos *= 2
    return ''.join(lines[-N:])


#-----------------TERMINATE PROCESSES CLEANLY------------------#

def destroy_process_children():
    active = mp.active_children()
    for child in active:
        child.terminate()
    return


#--------------------------------RESULT HANDLER FUNCTIONS--------------------------------#

def timed_logger_append(file_name, res):
    with open(file_name, "a") as file:
        file_log(file, res)
    return


def simple_logger_append(file_name, res):
    with open(file_name, "a") as file:
        file_write(file, res)
    return
    
    
def console_log(res):
    timed_res = append_time(res)
    print(timed_res)
    simple_logger_append(gp.CONSOLE_LOG_FILE_PATH, timed_res)
    return