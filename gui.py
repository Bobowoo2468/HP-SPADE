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
console_stored_count = -1

input_mode = 0

command_history = []
command_history_curs = -1

#-----------------------GLOBAL WIDGETS-----------------------#

app = App(title='prAUTO-testing', layout="grid")

toggle_input_button = PushButton(app, width=50, height=5, text="RTOS MODE", grid=[2,1], align="left") #SUBMIT BUTTON

user_input = TextBox(app, width=50, scrollbar=True, grid=[0,1], align="left")

cmd_log = TextBox(app, grid=[0,4,2,5], width=user_p.CMD_LOG_WIDTH, height=70, multiline=True, scrollbar=True)

rtos_log = TextBox(app, grid=[2,5], width=user_p.RTOS_LOG_WIDTH, height=70, multiline=True, scrollbar=True)

linux_log = TextBox(app, grid=[5,5], width=user_p.LINUX_LOG_WIDTH, height=70, multiline=True, scrollbar=True)

console_log = TextBox(app, grid=[7,5], width=user_p.CMD_LOG_WIDTH, height=70, multiline=True, scrollbar=True)


#-----------------------EVENT HANDLERS-----------------------#

def save_prev_commands(input_str):
    command_history.append(input_str)
    return

# DETECT 'ENTER' KEYSTROKE FOR EASE OF INPUT
def submit_on_enter(keypress_data, q):
    poll_and_transmit(q)
    return
    
# DETECT 'UP' KEYSTROKE TO RECALL CMD HISTORY
def up_handler(keypress_data, q):
    global command_history_curs
    
    if len(command_history) == 0:
        print("NO COMMANDS INPUT YET")
        return
    
    if command_history_curs == -1 and len(command_history) >= 1:
        command_history_curs = 0

    
    elif command_history_curs == 0:
        command_history_curs = len(command_history)-1
        
    else:
        command_history_curs -= 1
    
    user_input.value = command_history[command_history_curs]
    
        
# DETECT 'DOWN' KEYSTROKE TO RECALL CMD HISTORY
def down_handler(keypress_data, q):
    global command_history_curs
    
    if len(command_history) == 0:
        print("NO COMMANDS INPUT YET")
        return
    
    if command_history_curs == -1 and len(command_history) >= 1:
        command_history_curs = 0

    
    elif command_history_curs == len(command_history)-1:
        command_history_curs = 0
        
    else:
        command_history_curs += 1
    
    user_input.value = command_history[command_history_curs]     

# TOGGLE TRANSMISSION MODE FOR SERIAL 
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
        buffered_log = gf.get_last_Nlines(gp.RTOS_LOG_FILE_PATH, count-stored_count)
        rtos_log.value += buffered_log
        rtos_log.tk.yview_moveto('1')
        stored_count = count


def update_linux_log():
    global linux_stored_count
    
    count = gf.get_line_count(gp.LINUX_LOG_FILE_PATH)
    
    # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
    if count == linux_stored_count:
        return
    else:
        buffered_log = gf.get_last_Nlines(gp.LINUX_LOG_FILE_PATH, count-linux_stored_count)
        linux_log.value += buffered_log
        linux_log.tk.yview_moveto('1')
        linux_stored_count = count


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


def update_console_log():
    global console_stored_count
    
    count = gf.get_line_count(gp.CONSOLE_LOG_FILE_PATH)
    
    # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
    if count == console_stored_count:
        return
    else:
        buffered_log = gf.get_last_Nlines(gp.CONSOLE_LOG_FILE_PATH, count-console_stored_count)
        console_log.value += buffered_log
        console_log.tk.yview_moveto('1')
        console_stored_count = count

        
#-----------------------TRANSMIT RTOS/KERNEL COMMAND-----------------------#
        
def poll_and_transmit(q):
    global app, cmd_no, user_input, rtos_log, input_mode
    
    user_input_value = user_input.value
    save_prev_commands(user_input_value)
    parsed_whitespace_cmd = gf.remove_whitespace(user_input_value)
    
    if parsed_whitespace_cmd == "":
        return
    if parsed_whitespace_cmd == "EXIT":
        gf.destroy_process_children()
        app.destroy()
        sys.exit(0)
    
    if input_mode == gp.RTOS_MODE: 
        params_dict = {"key": "RTOS", "exec": "user_input", "dataline": parsed_whitespace_cmd}
    elif input_mode == gp.LINUX_MODE:
        params_dict = {"key": "LINUX", "exec": "user_input", "dataline": parsed_whitespace_cmd}
    q.put(params_dict)
    user_input.value, cmd_no = update_command_log(parsed_whitespace_cmd, input_mode, cmd_no, user_input_value)
    
#-----------------------DEFINE GUI LAYOUT-----------------------#

def gui_f(q):
    global app, cmd_no, user_input, cmd_log, rtos_log
    
    # DEFINE WIDGETS
    Text(app, text="Insert command here:", grid=[0,0], align="left") #USER INPUT LABEL
    Text(app, text="Command Log:", grid=[0,3], align="left") #COMMAND LOG LABEL
    Text(app, text="RTOS Log:", grid=[2,3], align="left") #RTOS LOG LABEL
    Text(app, text="Linux Log:", grid=[5,3], align="left") #LINUX LOG LABEL
    Text(app, text="Console Log:", grid=[7,3], align="left") #CONSOLE LOG LABEL
    
    # CONTINUOUSLY UPDATE SERIAL OUTPUTS FOR CONCURRENCY
    app.repeat(user_p.LOGGER_REFRESH_RATE, update_rtos_log)
    app.repeat(user_p.LOGGER_REFRESH_RATE, update_linux_log)
    app.repeat(user_p.LOGGER_REFRESH_RATE, update_console_log)
    
    PushButton(app, text="SEND COMMAND", command=poll_and_transmit, args=[q], grid=[0,2], align="left") #SUBMIT BUTTON
    
    # GUI EVENTS (KEYSTROKE DETECTION AND BUTTON CLICKS)
    # rtos_log.tk.vbar >> SCROLLBAR PROPERTY (TKINTER)
    user_input.tk.bind('<Return>', lambda event, arg=q: submit_on_enter(event, arg))
    user_input.tk.bind('<Up>', lambda event, arg=q: up_handler(event, arg))
    user_input.tk.bind('<Down>', lambda event, arg=q: down_handler(event, arg))
    toggle_input_button.when_clicked = toggle_rtos_linux_mode
    
    app.display()


