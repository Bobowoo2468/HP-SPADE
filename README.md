# HP-SPADE
HP SPADE (Automated Serial Printer DEbugger)  is designed to automate testing for HP Inkjet Printers by parsing serial output and automating transmit commands.

<img src="https://user-images.githubusercontent.com/62021897/204767735-a90c36b6-514b-4266-a25a-79b489c620e0.png" width=250 height=250/>

This project is one of the main deliverables of my electrical and electronics engineering (EE) internship at Hewlett-Packard (HP Inc.), to automate testing and debugging of printers.
This involves routing the serial output from the main processor into a python script with the help of a Raspberry Pi interface to allow receive and transmission of UART.
<br/>
<br/>

<b>Progress Made in the 1st Month</b>

<li>Real-time Keyword Detection and Execution of Corresponding Function Concurrently for two UART Channels</li>
<li>Logging Salient Data in CSV Format for Future Data Analysis</li>
<li>Quality-of-life Extensions for Improved User Experience (keystroke/hot-keys) and Command History</li>
<li>Clean GUI with Minimal Interactions powered by guizero</li>
<li>Integration of Hardware Sensors and Auxiliaries by Manipulating RPi GPIO (Wifi Attenuation)</li>
<li>OOP Code Structure for Ease of Future Development and Maintenance</li>
<li>Developer's Guide (in progress) for Customisations</li>

<br/>

The automated debugger uses Python's <b> multiprocessing </b> dependency, to allow concurrency between transmission of command, parsing, and GUI display.
Additionally, events and queues are used to maintain concurrency and shared data between multiple processes.

<br/>

![2022-12-22-140743_2560x1440_scrot](https://user-images.githubusercontent.com/62021897/209074430-e28a8b0f-8ab0-4cd4-9356-cc7731fd21ef.png)


<br/>
<br/>
<b>Stay tuned for more!</b>

