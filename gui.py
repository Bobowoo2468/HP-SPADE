from guizero import App, PushButton, Text, TextBox
import sys
import globalparams as gp
import globalfunctions as gf

#-----------------------IMPORT FROM USER DIRECTORY-----------------------#

from user import params as user_p
from user import functions as user_f

#-----------------------GLOBAL VARIABLES-----------------------#

cmd_no = 1
stored_count = -1
linux_stored_count = -1

#-----------------------GLOBAL WIDGETS-----------------------#

app = App(title='prAUTO-testing', layout="grid")

user_input = TextBox(app, width=50, scrollbar=True, grid=[0,1], align="left")

cmd_log = TextBox(app, grid=[0,4,2,5], width=75, height=70, multiline=True, scrollbar=True)

serial_log = TextBox(app, grid=[2,5], width=100, height=70, multiline=True, scrollbar=True)

linux_log = TextBox(app, grid=[5,5], width=100, height=70, multiline=True, scrollbar=True)

# serial_log.tk.vbar >> SCROLLBAR PROPERTY (TKINTER)

# DETECT ENTER KEYSTROKE FOR EASE OF INPUT
def submit_on_enter(event_data):
    if (event_data.key=='\r'):
        poll_and_transmit()

#-----------------------EVENT HANDLERS-----------------------#

def update_serial_log():
    global stored_count
    
    count = gf.get_line_count(gp.SERIAL_LOG_FILE_PATH)
    
    # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
    if count == stored_count:
        return
    else:
        stored_count = count
        last_line = gf.get_lastline(gp.SERIAL_LOG_FILE_PATH)
        serial_log.value += last_line
        serial_log.tk.yview_moveto('1')

def update_linux_log():
    global linux_stored_count
    
    count = gf.get_line_count(gp.LINUX_LOG_FILE_PATH)
    
    # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
    if count == linux_stored_count:
        return
    else:
        linux_stored_count = count
        last_line = gf.get_lastline(gp.LINUX_LOG_FILE_PATH)
        linux_log.value += last_line
        linux_log.tk.yview_moveto('1')
        

def poll_and_transmit():
    global app, cmd_no, user_input, cmd_log, serial_log
    
    parsed_whitespace_cmd = gf.remove_whitespace(user_input.value)
    
    if parsed_whitespace_cmd == "":
        return
    
    if parsed_whitespace_cmd == "EXIT":
        gf.destroy_process_children()
        app.destroy()
        sys.exit(0)
    
    else:
        gf.simple_logger_append(user_p.FILE_NAMES["command_log"], parsed_whitespace_cmd)
        gp.SER.write(gf.string_to_byte(parsed_whitespace_cmd))
        
    parsed_input_cmd = gf.parse_input_cmd(user_input.value, cmd_no)
    cmd_log.value += parsed_input_cmd
    user_input.value = ''
    cmd_no = cmd_no + 1

#-----------------------GUI INIT-----------------------#

def gui_f():
    global app, cmd_no, user_input, cmd_log, serial_log
    
    # WIDGETS
    Text(app, text="Insert command here:", grid=[0,0], align="left") #USER INPUT LABEL
    Text(app, text="Command Log:", grid=[0,3], align="left") #COMMAND LOG LABEL
    Text(app, text="Serial Log:", grid=[2,3], align="left") #SERIAL LOG LABEL
    Text(app, text="Linux Log:", grid=[5,3], align="left") #LINUX LOG LABEL
    
    PushButton(app, text="SEND COMMAND", command=poll_and_transmit, grid=[0,2], align="left") #SUBMIT BUTTON
    
    # GUI LOGIC
    user_input.when_key_pressed = submit_on_enter
    
    # PRINT SERIAL OUTPUTS
    app.repeat(4, update_serial_log)
    app.repeat(5, update_linux_log)
    
    app.display()


