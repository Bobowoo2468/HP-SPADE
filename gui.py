from guizero import App, PushButton, Text, TextBox, Slider
import sys
import functools
import globalparams as gp, globalfunctions as gf

#-----------------------IMPORT FROM USER DIRECTORY-----------------------#

from user import params as up
from user import functions as uf

class Gui():
    
    #-----------------------CLASS-LEVEL VARIABLES-----------------------#
    
    q = None
    wa = None
    stored_count = -1
    linux_stored_count = -1
    console_stored_count = -1
    command_stored_count = -1

    input_mode = 0

    command_history = []
    command_history_curs = -1
    
    app = App(title='HP Automated Serial Debugger', layout="grid")
    
    
    #-------------------------------------------GUI WIDGETS-------------------------------------------#
    
    #-----------------------INPUT WIDGETS-----------------------#
    
    toggle_input_button = PushButton(app, width=30, height=3, text="RTOS MODE", grid=[2,1], align="left") #SUBMIT BUTTON
    Text(app, text="Insert command here:", grid=[0,0], align="left") #USER INPUT LABEL
    user_input = TextBox(app, width=50, scrollbar=True, grid=[0,1], align="left")
    send_command_button = PushButton(app, text="SEND COMMAND", height=3, grid=[0,2], align="left") #SUBMIT BUTTON
    
    
    #-----------------------AUTOFILL WIDGETS-----------------------#
    
    autofill_button = PushButton(app, text="RTOS: udws 'nca.get_wireless_config'", grid=[0,7], width=30, height=3, align="right") 
    autofill_button_2 = PushButton(app, text="LINUX: restart", grid=[2,7], width=30, height=3, align="right")
    autofill_button_3 = PushButton(app, text="LINUX: iperf3 -s", grid=[3,7], width=30, height=3, align="right")
    
    #-----------------------PROGRAM STATUS WIDGETS-----------------------#
    
    start_auto_button = PushButton(app, text="START", grid=[3,0], width=30, height=3, align="right") #START PROGRAM
    stop_auto_button = PushButton(app, text="STOP", grid=[3,1], width=30, height=3, align="right") #STOP PROGRAM
    auto_debug_text = Text(app, text="Auto Debug Status:", grid=[4,0])
    auto_debug_status = Text(app, text="IN PROGRESS", grid=[5,0], align="left")
    auto_debug_status.text_color = "green"
    
    #-----------------------ATTENUATION CONTROL WIDGETS-----------------------#
    
    attenuation_control = Text(app, grid=[6,1], width=20, text="Attenuation: ")  #ATTENUATION VALUE DISPLAY
    slider = Slider(app, grid=[6,0], end=95)
    adj_attn_button = PushButton(app, text="SET ATTENUATION", height=3, grid=[6,2]) #SEND ATTENUATION VALUE
    
    
    #-----------------------LOG WIDGETS-----------------------#
    
    Text(app, text="Command Log:", grid=[0,3], align="left") #COMMAND LOG LABEL
    Text(app, text="RTOS Log:", grid=[2,3], align="left") #RTOS LOG LABEL
    Text(app, text="Linux Log:", grid=[4,3], align="left") #LINUX LOG LABEL
    Text(app, text="Console Log:", grid=[6,3], align="left") #CONSOLE LOG LABEL
    
    command_log = TextBox(app, grid=[0,4,2,2], width=up.CMD_LOG_WIDTH, height=50, multiline=True, scrollbar=True)
    rtos_log = TextBox(app, grid=[2,4,2,2], width=up.RTOS_LOG_WIDTH, height=50, multiline=True, scrollbar=True)
    linux_log = TextBox(app, grid=[4,4,2,2], width=up.LINUX_LOG_WIDTH, height=50, multiline=True, scrollbar=True)
    console_log = TextBox(app, grid=[6,4,2,2], width=up.CMD_LOG_WIDTH, height=50, multiline=True, scrollbar=True)
    
    
    #-------------------------------------------CLASS FUNCTIONS-------------------------------------------#
    
    #-----------------------ATTENUATION CONTROL-----------------------#
    
    def change_attn_value(self):
        self.attenuation_control.value = "WiFi Attenuation: " + str(self.slider.value)
        return
    
    
    def get_user_input_attenuation(self):
        return self.slider.value


    def adjust_attenuation_and_ping_wireless_config(self):
        user_input_attenuation_value = self.get_user_input_attenuation()
        self.wa.set_all_channels_attenuation(user_input_attenuation_value)
        return


    #-----------------------UPDATE LOGS-----------------------#
    
    def update_rtos_log(self):
        count = gf.get_line_count(gp.RTOS_LOG_FILE_PATH)
        
        # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
        if count <= self.stored_count:
            return
        else:
            buffered_log = gf.get_last_Nlines(gp.RTOS_LOG_FILE_PATH, count-self.stored_count)
            self.rtos_log.value += buffered_log
            self.rtos_log.tk.yview_moveto('1')
            self.stored_count = count
            

    def update_linux_log(self):
        count = gf.get_line_count(gp.LINUX_LOG_FILE_PATH) 
        
        # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
        if count <= self.linux_stored_count:
            return
        else:
            # UPDATE UI LOG WITH LINES FROM PREV CURSOR TO END OF FILE
            buffered_log = gf.get_last_Nlines(gp.LINUX_LOG_FILE_PATH, count-self.linux_stored_count)
            self.linux_log.value += buffered_log
            self.linux_log.tk.yview_moveto('1')
            self.linux_stored_count = count
            
            
    def update_console_log(self):
        count = gf.get_line_count(gp.CONSOLE_LOG_FILE_PATH)
        
        # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
        if count <= self.console_stored_count:
            return
        else:
            buffered_log = gf.get_last_Nlines(gp.CONSOLE_LOG_FILE_PATH, count-self.console_stored_count)
            self.console_log.value += buffered_log
            self.console_log.tk.yview_moveto('1') # STICK SCROLLBAR TO END OF WINDOW
            self.console_stored_count = count            


    def update_command_log(self):
        count = gf.get_line_count(gp.COMMAND_LOG_FILE_PATH)
        # IF NUMBER OF LINES IN FILE REMAINS THE SAME, DO NOT UPDATE SERIAL LOGGER
        if count <= self.command_stored_count:
            return
        else:
            buffered_log = gf.get_last_Nlines(gp.COMMAND_LOG_FILE_PATH, count-self.command_stored_count)
            self.command_log.value += buffered_log
            self.command_log.tk.yview_moveto('1') # STICK SCROLLBAR TO END OF WINDOW
            self.command_stored_count = count


    def send_command_log(self):
        if self.input_mode == gp.RTOS_MODE:
            prepend = gp.RTOS_PREPEND_INDICATOR 
        elif self.input_mode == gp.LINUX_MODE:
            prepend = gp.LINUX_PREPEND_INDICATOR
            
        parsed_cmd = gf.parse_input_cmd(self.user_input.value, prepend)
        
        gf.timed_log(gp.COMMAND_LOG_FILE_PATH, parsed_cmd)

        return ''
            

    #-----------------------SERIAL WRITE-----------------------#
    
    def autofill_command(self, event_data):
        button_text = event_data.widget.text 
        command = button_text.split(": ")[1]
        channel = button_text.split(": ")[0]
        
        if channel == "RTOS":    
            params_dict = {"key": "RTOS", "exec": "user_input", "dataline": command}
        elif channel == "LINUX":
            params_dict = {"key": "LINUX", "exec": "user_input", "dataline": command}
        self.q.put(params_dict)
        
        # UPDATE LOG FILES
        self.user_input.value = self.send_command_log()        
    
    
    def clean_process_termination(self):
        gf.destroy_process_children()
        self.app.destroy()
        sys.exit(0)
       
       
    def clear_logs(self):
        self.rtos_log.value = ""
        self.linux_log.value = ""
        self.command_log.value = ""
        self.console_log.value = ""
        self.user_input.value = ""
        return
            
    def send_command(self):
        self.save_prev_commands(self.user_input.value) # STORE SENT COMMANDS
        
        parsed_whitespace_cmd = gf.remove_whitespace(self.user_input.value) # REMOVE WHITESPACE FROM COMMANDS
        
        if parsed_whitespace_cmd == "":
            return
        
        # CLEAR UI LOGS
        if parsed_whitespace_cmd == "CLEAR":
            self.clear_logs()
            return
        
        if parsed_whitespace_cmd == "RESTART":
            gf.gpio_pulldown()
            self.user_input.value = ""
            return
        
        # CLEAN PROCESS TERMINATION WITH KEYWORD "EXIT"
        if parsed_whitespace_cmd == "EXIT":
            self.clean_process_termination()
        
        # SEND USER INPUT COMMANDS TO END OF QUEUE
        if self.input_mode == gp.RTOS_MODE: 
            params_dict = {"key": "RTOS", "exec": "user_input", "dataline": parsed_whitespace_cmd}
        elif self.input_mode == gp.LINUX_MODE:
            params_dict = {"key": "LINUX", "exec": "user_input", "dataline": parsed_whitespace_cmd}
        self.q.put(params_dict)
        
        # UPDATE LOG FILES
        self.user_input.value = self.send_command_log()


    def toggle_rtos_linux_mode(self):
        if self.input_mode == 0:
            self.toggle_input_button.text = "LINUX MODE"
            self.input_mode = 1
        else:
            self.toggle_input_button.text = "RTOS MODE"
            self.input_mode = 0
        return


    #-----------------------KEYSTROKE HANDLING/QUALITY OF LIFE-----------------------#
        
    def save_prev_commands(self, input_str):
        self.command_history.append(input_str)
        return


    # DETECT 'ENTER' KEYSTROKE FOR EASE OF INPUT
    def send_command_on_enter(self, e):
        self.send_command()
        return
        
        
    # DETECT 'UP' KEYSTROKE TO RECALL CMD HISTORY
    def up_handler(self, e):
        # NO COMMANDS TO RETRIEVE
        if len(self.command_history) == 0:
            return
        
        if self.command_history_curs == -1 and len(self.command_history) >= 1:
            self.command_history_curs = 0

        
        elif self.command_history_curs == 0:
            self.command_history_curs = len(self.command_history)-1
        
        else:
            self.command_history_curs -= 1
        
        # LOAD STORED COMMANDS
        self.user_input.value = self.command_history[self.command_history_curs]
        
            
    # DETECT 'DOWN' KEYSTROKE TO RECALL CMD HISTORY
    def down_handler(self, e):
        # NO COMMANDS TO RETRIEVE
        if len(self.command_history) == 0:
            return
        
        if self.command_history_curs == -1 and len(self.command_history) >= 1:
            self.command_history_curs = 0

        
        elif self.command_history_curs == len(self.command_history)-1:
            self.command_history_curs = 0
            
        else:
            self.command_history_curs += 1
        
        # LOAD STORED COMMANDS
        self.user_input.value = self.command_history[self.command_history_curs]     


    def terminate_interrupt(self, e):
        if self.input_mode == 1:
            gp.LINUX.write(b'\x03')
        elif self.input_mode == 0:
            gp.RTOS.write(b'\x03')
        gf.console_log("ESCAPED")
        return
        
        
    #-----------------------PROGRAM CONTROL-----------------------#
    
    def start_auto_debug(self):
        if gp.in_progress_flag == 1:
            gf.console_log("AUTO DEBUGGER ALREADY RUNNING")
            return

        self.q.put("START")
        self.auto_debug_status.value = "IN PROGRESS"
        self.auto_debug_status.text_color = "green"
        gp.in_progress_flag = 1
        return


    def stop_auto_debug(self):
        if gp.in_progress_flag == 0:
            gf.console_log("AUTO DEBUGGER ALREADY STOPPED")
            return
        
        # CLEARS QUEUE
        while not self.q.empty():
            self.q.get_nowait()
        
        # ENQUEUE SENTINEL TO HALT PROGRAM
        self.q.put(None)
        self.auto_debug_status.value = "STOPPED"
        self.auto_debug_status.text_color = "red"    
        gp.in_progress_flag = 0
        return
         

    #-------------------------------------------MAIN EXECUTION-------------------------------------------#

    
    def __init__(self, q, wa):

        self.q = q
        self.wa = wa
        self.slider.value = 0
        
        if wa is False:
            self.adj_attn_button.hide()
            self.slider.hide()
            self.attenuation_control.hide()
        
        #-----------------------LOGIC INSERTS-----------------------#
        
        # CONTINUOUSLY UPDATE SERIAL OUTPUTS FOR CONCURRENCY
        self.app.repeat(up.LOGGER_REFRESH_RATE, self.update_rtos_log)
        self.app.repeat(up.LOGGER_REFRESH_RATE, self.update_linux_log)
        self.app.repeat(up.LOGGER_REFRESH_RATE, self.update_console_log)
        self.app.repeat(up.LOGGER_REFRESH_RATE, self.update_command_log)
        
        self.toggle_input_button.when_clicked = self.toggle_rtos_linux_mode
        self.send_command_button.when_clicked = self.send_command
        self.start_auto_button.when_clicked = self.start_auto_debug
        self.stop_auto_button.when_clicked = self.stop_auto_debug
        self.adj_attn_button.when_clicked = self.adjust_attenuation_and_ping_wireless_config
        self.slider.when_mouse_dragged = self.change_attn_value
        self.slider.when_left_button_released = self.change_attn_value
        self.autofill_button.when_clicked = self.autofill_command
        self.autofill_button_2.when_clicked = self.autofill_command
        self.autofill_button_3.when_clicked = self.autofill_command
        
        # GUI EVENTS (KEYSTROKE DETECTION AND BUTTON CLICKS)
        # rtos_log.tk.vbar >> SCROLLBAR PROPERTY (TKINTER)
        self.user_input.tk.bind('<Return>', self.send_command_on_enter)
        self.user_input.tk.bind('<Up>', self.up_handler)
        self.user_input.tk.bind('<Down>', self.down_handler)
        self.user_input.tk.bind('<Escape>', self.terminate_interrupt)

        self.app.display()

