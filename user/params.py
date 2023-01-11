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
    "restart": "logs/restart.txt",
    "throughput": "logs/throughput.txt"
}

# COMPLETE LIST OF FILE NAMES
FILE_NAMES = {
    "linux_log": "logs/linuxlog.txt",
    "serial_log": "logs/seriallog.txt",
    "signal_strength": "logs/signalstrength.txt",
    "command_log": "logs/commandlog.txt",
    "noise": "logs/noise.txt",
    "console_log": "logs/consolelog.txt",
    "restart": "logs/restart.txt",
    "throughput": "logs/throughput.txt"
}


FILE_HEADERS = {
    "logs/signalstrength.txt": "Timestamp,WiFi Attenuation,Signal Strength\n",
    "logs/throughput.txt": "Timestamp,WiFi Attenuation,Signal Strength,Noise,Transfer Rate,Bandwidth\n",
    "logs/noise.txt": "Timestamp,WiFi Attenuation,Noise\n"
}


#-----------------------KEYWORD AND CORRESPONDING FUNCTIONS DICTIONARY-----------------------#

# "KEYWORD": "CORRESPONDING FUNCTION NAME"
KEYWORD_DICTIONARY = {
    "signalStrength": 'adjust_attenuation_and_ping_wifi',
    "noise": 'log_wireless_config_noise'
}

LINUX_KEYWORD_DICTIONARY = {
    "bits/sec": 'log_throughput',
    "cfg80211_disconnected": 'wifi_disconnected',
    "wl_bss_connect_done succeeded": 'wifi_reconnected'
}

SIGNALSTRENGTH_DICTIONARY = {
    "signalStrength": 'ping_wireless_config',
    "noise": 'log_wireless_config_noise'
}

RESTART_ASSERT_DICTIONARY = {
    "going mute:": 'restart',
    "asserted": 'halt_restart'
}

MVP1_RTOS = {
    "going mute:": 'restart'
}

MVP1_LINUX = {
    "/dev/btusb0": 'restart_success_factor_one',
    "encfs exit status = 0": 'restart_success_factor_two'
}

MVP2_RTOS = {
    "signalStrength": 'adjust_attenuation_and_ping_wifi',
    "noise": 'log_wireless_config_noise'
}

MVP2_LINUX = {
    "bits/sec": 'log_throughput',
    "cfg80211_disconnected": 'wifi_disconnected',
    "wl_bss_connect_done succeeded": 'wifi_reconnected'
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

LOGGER_REFRESH_RATE = 100 # (in ms) 

CMD_LOG_WIDTH = 50
CONSOLE_LOG_WIDTH = 50
RTOS_LOG_WIDTH = 75
LINUX_LOG_WIDTH = 75


#----------------------MVP2 (WIFI ATTENUATION) PARAMS----------------------#

PING_NO = 10
MAX_ATTENUATION = 30
