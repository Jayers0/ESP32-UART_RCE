import machine
import time

uart = machine.UART(1, baudrate=115200, tx=17) 

while True:
    command_to_send = "print('Hello from sender!')"
    uart.write(command_to_send)
    time.sleep(1)

