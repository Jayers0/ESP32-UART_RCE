import machine
import time

uart = machine.UART(1, baudrate=115200, rx=16) 
while True:
    if uart.any():
        data_received = uart.read(uart.any())
        received_command = data_received.decode('utf-8').strip()
        print("Received command:", received_command)
        
        try:
            # Execute the received command using exec
            exec(received_command)
        except Exception as e:
            print("Error executing command:", e)
        
    time.sleep(1)

