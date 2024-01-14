import machine
from machine import Pin
import ujson
import time

# Configure UART and LED pin
uart = machine.UART(1, baudrate=115200, rx=16)  # Change rx pin as per your ESP32 board
led_pin = Pin(2, Pin.OUT)
led_pin.on()

# Global variables
memory_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
device_id = 1

def flash_led(duration=0.1):
    # Flash the LED for a specified duration
    led_pin.value(1)
    time.sleep(duration)
    led_pin.value(0)

def manage_memory(data):
    global device_id

    print("Received memory information:", data)

    try:
        # Concatenate received lines until a complete JSON string is obtained
        while data.count('{') > data.count('}'):
            if uart.any():
                data += uart.read(uart.any()).decode('utf-8')

        # Deserialize the JSON data back into a dictionary
        received_memory_info_dict = ujson.loads(data)
        
        # Process the received memory information as needed
        for received_device_id, info in received_memory_info_dict.items():
            print(f"Device ID: {received_device_id}, Data: {info['data']}")
            perform_memory_operation(received_device_id, info)
    except Exception as e:
        print("Error processing received data:", e)

def perform_memory_operation(received_device_id, data):
    global memory_data
    global device_id

    # Extracting nested data for the specified device ID
    nested_data = data.get(received_device_id, {}).get('data', {})
    start_index = nested_data.get("start_index", 0)
    stop_index = nested_data.get("stop_index", 0)
    operation_code = nested_data.get("operation_code", 0)

    if operation_code == 1:
        print(f"Copying and sending data for Device ID {received_device_id} from index {start_index} to {stop_index}")
        # Implement the logic for copying and sending data over UART
    elif operation_code == 2:
        print(f"Deleting and replacing data for Device ID {received_device_id} from index {start_index} to {stop_index}")
        memory_data[start_index:stop_index] = [0] * (stop_index - start_index)
        # Implement the logic for deleting and replacing data
    elif operation_code == 0:
        print(f"No-Op for Device ID {received_device_id}")
    elif operation_code == 3:
        print(f"Custom code execution for Device ID {received_device_id}")
        custom_code = nested_data.get("code", "")
        try:
            # Execute the custom code using exec with memory_data as a target
            exec(custom_code, {"memory_data": memory_data, "device_id": received_device_id})
        except Exception as e:
            print(f"Error executing custom code for Device ID {received_device_id}: {e}")
    else:
        print(f"Unknown operation code for Device ID {received_device_id}")

def main():
    global device_id
    print(f"Initial Device ID: {device_id}\nInitial Memory Data: {memory_data}")

    while True:
        if uart.any():
            data_received = uart.read(uart.any())
            flash_led()  # Flash the LED when data is received
            received_data = data_received.decode('utf-8').strip()
            print("Received data:", received_data)
            manage_memory(received_data)

        device_id = 1 if device_id == 4 else device_id + 1
        time.sleep(1)

if __name__ == "__main__":
    main()
