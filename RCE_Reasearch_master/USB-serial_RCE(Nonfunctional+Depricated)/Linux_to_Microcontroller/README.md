# Interoperability of MicroPython and Python Scripts for ESP32

This set of programs demonstrates a basic interoperability scenario between MicroPython running on an ESP32 microcontroller and a Python script running on a computer.

### Program: `USB-UART-POC.py`

This MicroPython program reads code from the USB0 UART on the ESP32 until it encounters an EOF (End of File) character (Ctrl-D) and then executes the code using `eval`.
**THIS NEEDS TO BE CHANGED LATER AWAY FROM EVAL**

#### Usage:

1. Upload the `esp32_uart_code_executor.py` program to your ESP32 running MicroPython. 
**I USED THONNY FOR THIS HOWEVER THE 'esptool.py' Util**
2. Connect your ESP32 to the computer via USB.
3. Open a serial terminal to view the ESP32 output (e.g., `screen /dev/ttyUSB0 115200`).
4. Run the Python script on your computer to send code to the ESP32.

## Python Script (Computer)

### Script: `Linux_to_ESP32.py`

This Python script reads the contents of a specified file, sends it over USB0 UART to the ESP32, and awaits the response.

#### Usage:

1. Make sure you have Python and the `pyserial` library installed (`pip install pyserial`).
2. Run the Python script, providing the path to the file you want to send.

   ```bash
   python3 Linux_To_ESP32.py path/to/your/file.py
   ```
   
Replace path/to/your/file.py with the actual path to the file you want to send to the ESP32.

Monitor the ESP32 output on the serial terminal for the execution result.
Note: Ensure the ESP32 is connected to the correct serial port (/dev/ttyUSB0 by default). Adjust the port variable in the Python script if necessary.
