import serial

# SYNC PRINTER BAUDRATE 115.2KBPS
BAUD_RATE = 115200

# SERIAL PORTS - CHECK PORT AVAILABILITY WITH "ls -l/dev/tty*" IN TERMINAL
RTOS_PATH = "/dev/ttyAMA1"
LINUX_PATH = "/dev/ttyAMA2"

# DEFINE pySerial OBJECT TO SET UP SEPARATE SERIAL PORT CONNECTIONS
RTOS = serial.Serial(port=RTOS_PATH, baudrate=BAUD_RATE, timeout=5)
LINUX = serial.Serial(port=LINUX_PATH, baudrate=BAUD_RATE, timeout=5)

# USER API DIRECTORY
USER_DIRECTORY = '/home/eelab/Documents/woobotuan/MVP3/user'

RTOS_LOG_FILE_PATH = 'logs/seriallog.txt'
LINUX_LOG_FILE_PATH = 'logs/linuxlog.txt'
CONSOLE_LOG_FILE_PATH = 'logs/consolelog.txt'

RTOS_MODE = 0
LINUX_MODE = 1

RTOS_PREPEND_INDICATOR = "#"
LINUX_PREPEND_INDICATOR = "X"