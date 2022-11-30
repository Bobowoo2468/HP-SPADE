import serial

# SYNC PRINTER BAUDRATE 115.2KBPS
BAUD_RATE = 115200

SERIAL_PATH = "/dev/ttyAMA1"
LINUX_PATH = "/dev/ttyAMA2"

SER = serial.Serial(port=SERIAL_PATH, baudrate=BAUD_RATE, timeout=5)
LINUX = serial.Serial(port=LINUX_PATH, baudrate=BAUD_RATE, timeout=5)

USER_DIRECTORY = '/home/eelab/Documents/woobotuan/MVP2/user'

SERIAL_LOG_FILE_PATH = 'logs/seriallog.txt'
LINUX_LOG_FILE_PATH = 'logs/linuxlog.txt'