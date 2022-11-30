from guizero import App, PushButton, Text, TextBox
from datetime import datetime
import os, sys
import globalparams as gp
import globalfunctions as gf

#-----------------------GLOBAL VARIABLES-----------------------#

cmd_no = 1

app = App(title='prAUTO-testing', layout="grid")

input_cmd = TextBox(app, width=50, scrollbar=True, grid=[0,1], align="left")

log = TextBox(app, grid=[0,4,2,5], width=100, height=100, multiline=True, scrollbar=True)

serial_output = TextBox(app, grid=[10,5], width=200, height=100, multiline=True, scrollbar=True)

# serial_output.tk.vbar - Scrollbar Tkinter Property

stored_count = 0

#-----------------------STRING PARSERS-----------------------#

# DETECT ENTER KEYSTROKE FOR EASE OF INPUT
def submit_on_enter(event_data):
    if (event_data.key=='\r'):
        poll_and_transmit()

# PARSE INPUT COMMAND WITH DATETIME
def parse_input_cmd(string, cmd_no):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    parsed_input = "Command " + str(cmd_no) + ": "  + str(current_time) + " - " + string.rstrip().lstrip() + "\n"
    return parsed_input

def remove_whitespace(string):
    return "".join(string.rstrip().lstrip())

#-----------------------EVENT HANDLERS-----------------------#

def update_label():
    global stored_count
    count = -1
    
    with open(gp.WRITE_FILE_NAME, 'rb') as fp:
        for count, line in enumerate(fp):
            pass
    
    if count == stored_count:
        return
    else:
        stored_count = count
    
    with open(gp.WRITE_FILE_NAME, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
                
        except OSError:
            f.seek(0)

        last_line = f.readline().decode()
        serial_output.value += last_line
        serial_output.tk.yview_moveto('1')

def poll_and_transmit():
    global app
    global cmd_no
    global input_cmd
    global log
    global serial_output
    
    parsed_whitespace_cmd = remove_whitespace(input_cmd.value)
    
    if parsed_whitespace_cmd == "":
        return
    
    if parsed_whitespace_cmd == "EXIT":
        app.destroy()
        sys.exit(0)
    
    else:
        print ("ECHO: " + parsed_whitespace_cmd) 
        gp.SER.write(gf.string_to_byte(parsed_whitespace_cmd))
        
    parsed_input_cmd = parse_input_cmd(input_cmd.value, cmd_no)
    log.value += parsed_input_cmd
    input_cmd.value = ''
    cmd_no = cmd_no + 1

#-----------------------GUI INIT-----------------------#

def gui_f():
    global app
    global cmd_no
    global input_cmd
    global log
    global serial_output
    
    input_cmd_label = Text(app, text="Insert command here:", grid=[0,0], align="left")
    log_label = Text(app, text="Commands sent here:", grid=[0,3], align="left")
    serial_output_label = Text(app, text="Serial output here:", grid=[10,0], align="left")

    send_command = PushButton(app, text="SEND COMMAND", command=poll_and_transmit, grid=[0,2], align="left")
    input_cmd.when_key_pressed = submit_on_enter
    
    app.repeat(20, update_label)
    app.display()


