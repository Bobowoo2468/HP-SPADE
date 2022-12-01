import serial

FILE_NAMES = {
    "serial_log": "logs/seriallog.txt",
    "signal_strength": "logs/signalstrength.txt",
    "command_log": "logs/commandlog.txt"
}

# "KEYWORD": "CORRESPONDING FUNCTION NAME"
KEYWORD_DICTIONARY = {
    "Power": 'ping_wireless_scan',
    "signalStrength": 'ping_wireless_config',
    "noise": 'ping_wireless_config'
}