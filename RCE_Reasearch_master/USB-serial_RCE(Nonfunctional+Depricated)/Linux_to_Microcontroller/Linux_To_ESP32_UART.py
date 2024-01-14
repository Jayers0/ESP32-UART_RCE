import argparse
import serial
import time

def is_esp32_connected(port='/dev/ttyUSB1', baudrate=9600):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            return True
    except serial.SerialException:
        return False

#
def send_file_over_uart(file_path, port='/dev/ttyUSB0', baudrate=9600):
    # Check if ESP32 is connected
    if not is_esp32_connected(port, baudrate):
        print("ESP32 not detected on the specified port. Please check the connection.")
        return 
    else:
        print("ESP32 is connected on: ",port,"\nBaudrate: ",baudrate)

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        code = file.read()

    # Open the serial connection
    # Inside send_file_over_uart function
    with serial.Serial(port, baudrate, timeout=1, rtscts=False) as ser:


        # Send each character of the code over UART
        for char in code:
            ser.write(char.encode('utf-8'))
            #time.sleep(0.01)  # Adjust sleep duration based on your ESP32's processing speed

        # Send EOF (Ctrl-D) to indicate the end of the code
        ser.write(b'\x04')  # Change to the correct EOF character
        response =""
        # Wait for the response
        while ser.readline().decode() != '\x04':
            response += ser.readline().decode('utf-8')
            if response == "":
                print("no response from ESP32")
            else:
                print("Response from ESP32:{", response,"}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a file over USB0 UART to ESP32 and await response.")
    parser.add_argument("file_path", help="Path to the file to send over UART")

    args = parser.parse_args()

    send_file_over_uart(args.file_path)
