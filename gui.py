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
input_mode = 0

#-----------------------GLOBAL WIDGETS-----------------------#

app = App(title='prAUTO-testing', layout="grid")

toggle_input_button = PushButton(app, width=50, height=5, text="RTOS MODE", grid=[2,1], align="left") #SUBMIT BUTTON

user_input = TextBox(app, width=50, scrollbar=True, grid=[0,1], align="left")

cmd_log = TextBox(app, grid=[0,4,2,5], width=75, height=70, multiline=True, scrollbar=True)

rtos_log = TextBox(app, grid=[2,5], width=100, height=70, multiline=True, scrollbar=True)

linux_log = TextBox(app, grid=[5,5], width=100, height=70, multiline=True, scrollbar=True)

# rtos_log.tk.vbar >> SCROLLBAR PROPERTY (TKINTER)

# DETECT ENTER KEYSTROKE FOR EASE OF INPUT
def submit_on_enter(event_data):
    if (event_data.key=='\r'):
        poll_and_transmit()

#-----------------------EVENT HANDLERS-----------------------#
        
def toggle_rtos_linux_mode():
    global input_mode
    if input_mode == 0:
        toggle_input_button.text = "LINUX MODE"
        input_mode = 1
    else:
        toggle_input_button.text = "RTOS MODE"
        input_mode = 0
    return

    #-----------------------CONTINUAL UPDATE OF LOGS ON GUI-----------------------#

def update_rtos_log():
    global stored_count
    
    count = gf.get_line_count(gp.RTOS_LOG_FILE_PATH)
    
    # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
    if count == stored_count:
        return
    else:
        stored_count = count
        last_line = gf.get_lastline(gp.RTOS_LOG_FILE_PATH)
        rtos_log.value += gf.append_time(last_line)
        rtos_log.tk.yview_moveto('1')

def update_linux_log():
    global linux_stored_count
    
    count = gf.get_line_count(gp.LINUX_LOG_FILE_PATH)
    
    # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
    if count == linux_stored_count:
        return
    else:
        linux_stored_count = count
        last_line = gf.get_lastline(gp.LINUX_LOG_FILE_PATH)
        linux_log.value += gf.append_time(last_line)
        linux_log.tk.yview_moveto('1')

def update_command_log(cmd, input_mode, cmd_no, user_input_value):
    global cmd_log
    if input_mode == gp.RTOS_MODE:
        prepend = gp.RTOS_PREPEND_INDICATOR 
    elif input_mode == gp.LINUX_MODE:
        prepend = gp.LINUX_PREPEND_INDICATOR
    parsed_cmd = gf.parse_input_cmd(user_input_value, cmd_no, prepend)
    
    gf.simple_logger_append(user_p.FILE_NAMES["command_log"], parsed_cmd)
    cmd_log.value += parsed_cmd
    return '', cmd_no+1 
    
        
    #-----------------------TRANSMIT RTOS/KERNEL COMMAND-----------------------#
        
def poll_and_transmit():
    global app, cmd_no, user_input, rtos_log, input_mode
    
    user_input_value = user_input.value
    parsed_whitespace_cmd = gf.remove_whitespace(user_input_value)
    
    if parsed_whitespace_cmd == "":
        return
    if parsed_whitespace_cmd == "EXIT":
        gf.destroy_process_children()
        app.destroy()
        sys.exit(0)
    
    if input_mode == gp.RTOS_MODE: 
        gp.RTOS.write(gf.string_to_byte(parsed_whitespace_cmd))
    elif input_mode == gp.LINUX_MODE:
        gp.LINUX.write(gf.string_to_byte(parsed_whitespace_cmd))       
    
    user_input.value, cmd_no = update_command_log(parsed_whitespace_cmd, input_mode, cmd_no, user_input_value)
    
#-----------------------GUI INIT-----------------------#

def gui_f():
    global app, cmd_no, user_input, cmd_log, rtos_log
    
    # WIDGETS
    Text(app, text="Insert command here:", grid=[0,0], align="left") #USER INPUT LABEL
    Text(app, text="Command Log:", grid=[0,3], align="left") #COMMAND LOG LABEL
    Text(app, text="RTOS Log:", grid=[2,3], align="left") #RTOS LOG LABEL
    Text(app, text="Linux Log:", grid=[5,3], align="left") #LINUX LOG LABEL
    
    PushButton(app, text="SEND COMMAND", command=poll_and_transmit, grid=[0,2], align="left") #SUBMIT BUTTON
    
    # GUI LOGIC
    user_input.when_key_pressed = submit_on_enter
    
    toggle_input_button.when_clicked = toggle_rtos_linux_mode
    
    # PRINT SERIAL OUTPUTS
    app.repeat(10, update_rtos_log)
    app.repeat(10, update_linux_log)
    
    app.display()


