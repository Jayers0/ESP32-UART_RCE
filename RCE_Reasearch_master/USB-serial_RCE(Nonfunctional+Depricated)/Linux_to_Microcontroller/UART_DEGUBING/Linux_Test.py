# send_test_code.py

import argparse
import serial
import time

def send_code_over_uart(code, port='/dev/ttyUSB0', baudrate=115200):
    # Open the serial connection
    with serial.Serial(port, baudrate, timeout=1) as ser:
        # Send each character of the code over UART
        for char in code:
            ser.write(char.encode('utf-8'))
            time.sleep(0.01)  # Adjust sleep duration based on your ESP32's processing speed
       

        # Wait for the response on repl
        print("sending char")

if __name__ == "__main__":


    # Send the test code over UART

    while True:
        send_code_over_uart('c')
