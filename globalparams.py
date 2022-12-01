import serial

# SYNC PRINTER BAUDRATE 115.2KBPS
BAUD_RATE = 115200

RTOS_PATH = "/dev/ttyAMA1"
LINUX_PATH = "/dev/ttyAMA2"

RTOS = serial.Serial(port=RTOS_PATH, baudrate=BAUD_RATE, timeout=5)
LINUX = serial.Serial(port=LINUX_PATH, baudrate=BAUD_RATE, timeout=5)

USER_DIRECTORY = '/home/eelab/Documents/woobotuan/MVP2/user'

RTOS_LOG_FILE_PATH = 'logs/seriallog.txt'
LINUX_LOG_FILE_PATH = 'logs/linuxlog.txt'

RTOS_MODE = 0
LINUX_MODE = 1

RTOS_PREPEND_INDICATOR = "#"
LINUX_PREPEND_INDICATOR = "X"