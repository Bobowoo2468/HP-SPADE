import serial

#-----------------------DICTIONARY OF FILEPATHS-----------------------#

# FILE NAMES TO BE CLEARED AT THE START OF THE PROGRAM
CLEAR_FILE_NAMES = {
    "linux_log": "logs/linuxlog.txt",
    "serial_log": "logs/seriallog.txt",
    "signal_strength": "logs/signalstrength.txt",
    "command_log": "logs/commandlog.txt",
    "noise": "logs/noise.txt",
    "console_log": "logs/consolelog.txt",
    "restart": "logs/restart.txt"
}

# COMPLETE LIST OF FILE NAMES
FILE_NAMES = {
    "linux_log": "logs/linuxlog.txt",
    "serial_log": "logs/seriallog.txt",
    "signal_strength": "logs/signalstrength.txt",
    "command_log": "logs/commandlog.txt",
    "noise": "logs/noise.txt",
    "console_log": "logs/consolelog.txt",
    "restart": "logs/restart.txt"
}


#-----------------------KEYWORD AND CORRESPONDING FUNCTIONS DICTIONARY-----------------------#

# "KEYWORD": "CORRESPONDING FUNCTION NAME"
KEYWORD_DICTIONARY = {
    "signalStrength": 'adjust_attenuation_and_ping_wifi',
    "noise": 'log_wireless_config_noise'
}

LINUX_KEYWORD_DICTIONARY = {

}

SIGNALSTRENGTH_DICTIONARY = {
    "signalStrength": 'ping_wireless_config',
    "noise": 'log_wireless_config_noise'
}

RESTART_ASSERT_DICTIONARY = {
    "going mute:": 'restart',
    "asserted": 'halt_restart'
}

BACKUP_DICTIONARY_RTOS = {
    "going mute:": 'restart'
}

BACKUP_DICTIONARY_LINUX = {
    "Shutdown": 'shutdown_success',
    "/dev/btusb0": 'restart_success'
}


#-----------------------RTOS COMMANDS-----------------------#

GET_WIFI_CONFIG = 'udws "nca.get_wireless_config"'
GET_WIFI_SCAN = 'udws "nca.get_wireless_scan"'


#----------------------FLAGS----------------------#

assert_flag = 0
stop_restart_flag = 0


#----------------------COUNT----------------------#

restart_count = 0


#----------------------GUI SETTINGS----------------------#

LOGGER_REFRESH_RATE = 100 # (in ms) NOTE: FASTEST POSSIBLE WITHOUT SYSTEM HANG AND OVERHEATING: 50

CMD_LOG_WIDTH = 50
CONSOLE_LOG_WIDTH = 50
RTOS_LOG_WIDTH = 75
LINUX_LOG_WIDTH = 75


#----------------------MVP2 (WIFI ATTENUATION) PARAMS----------------------#

PING_NO = 7
MAX_ATTENUATION = 50
