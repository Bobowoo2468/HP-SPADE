import serial

WRITE_FILE_NAME = "serialdump.txt"
SIGNAL_STRENGTH_FILE_NAME = "signalstrength.txt"

# SYNC PRINTER BAUDRATE 115.2KBPS
BAUD_RATE = 115200

SERIAL_PATH = "/dev/ttyS0"

SER = serial.Serial(port=SERIAL_PATH, baudrate=BAUD_RATE, timeout=5)

# "KEYWORD": "CORRESPONDING FUNCTION NAME"
KEYWORD_DICTIONARY = {
    "Power": 'ping_wireless_scan',
    "signalStrength": 'ping_wireless_config',
    "noise": 'ping_wireless_config',
    "restart": 'restart'
}
