# HP-SPADE
HP SPADE (Automated Serial Printer DEbugger)  is designed to automate testing for HP Inkjet Printers by parsing serial output and automating transmit commands.

This project is one of the main deliverables of my electrical and electronics engineering (EE) internship at Hewlett-Packard (HP Inc.), to automate testing and debugging of printers.
This involves routing the serial output from the main processor into a python script with the help of a Raspberry Pi interface to allow receive and transmission of UART.

The current progress made is a simple GUI with a input textfield allowing transmission of commands (including wifi detection, rebooting the printer etc.), as well as 
three output loggers showing the output from RTOS, Linux Kernel and the commands input by the user. 
Minimal output parsing has also been completed, allowing keyword detection and triggering of response on keyword detection.
Task has involved the use of python's <b> multiprocessing </b> dependency, to allow concurrency between transmission of command, parsing, and GUI display.

Stay tuned for more!

![image](https://user-images.githubusercontent.com/62021897/204767735-a90c36b6-514b-4266-a25a-79b489c620e0.png)
