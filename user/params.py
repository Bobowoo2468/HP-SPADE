import serial

#-----------------------DICTIONARY OF FILEPATHS-----------------------#

FILE_NAMES = {
    "linux_log": "logs/linuxlog.txt",
    "serial_log": "logs/seriallog.txt",
    "signal_strength": "logs/signalstrength.txt",
    "command_log": "logs/commandlog.txt",
    "noise": "logs/noise.txt"
}

#-----------------------KEYWORD AND CORRESPONDING FUNCTIONS DICTIONARY-----------------------#

# "KEYWORD": "CORRESPONDING FUNCTION NAME"
KEYWORD_DICTIONARY = {
    "signalStrength": 'ping_wireless_config',
    "noise": 'log_wireless_config_noise',
    "going mute:": 'restart',
    "asserted": 'halt_restart'
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