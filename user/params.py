import serial

#-----------------------DICTIONARY OF FILEPATHS-----------------------#

FILE_NAMES = {
    "linux_log": "logs/linuxlog.txt",
    "serial_log": "logs/seriallog.txt",
    "signal_strength": "logs/signalstrength.txt",
    "command_log": "logs/commandlog.txt",
    "noise": "logs/noise.txt",
    "console_log": "logs/consolelog.txt"
}

#-----------------------KEYWORD AND CORRESPONDING FUNCTIONS DICTIONARY-----------------------#

# "KEYWORD": "CORRESPONDING FUNCTION NAME"
KEYWORD_DICTIONARY = {
    "signalStrength": 'ping_wireless_config',
    "noise": 'log_wireless_config_noise',
    "going mute:": 'restart',
    "asserted": 'halt_restart'
}

LINUX_KEYWORD_DICTIONARY = {
#     "test": 'empty_test'  
}

SIGNALSTRENGTH_DICTIONARY = {
    "signalStrength": 'ping_wireless_config',
    "noise": 'log_wireless_config_noise'
}

RESTART_ASSERT_DICTIONARY = {
    "going mute:": 'restart',
    "asserted": 'halt_restart'
}

#----------------------FLAGS----------------------#

assert_flag = 0

#----------------------GUI SETTINGS----------------------#

LOGGER_REFRESH_RATE = 200 # (in ms) NOTE: FASTEST POSSIBLE WITHOUT SYSTEM HANG AND OVERHEATING: 50

CMD_LOG_WIDTH = 50
CONSOLE_LOG_WIDTH = 50
RTOS_LOG_WIDTH = 75
LINUX_LOG_WIDTH = 75
