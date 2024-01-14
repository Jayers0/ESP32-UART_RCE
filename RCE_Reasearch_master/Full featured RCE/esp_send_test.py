import machine
import ujson
import time

def send_memory_info(uart, memory_info_dict):
    # Serialize the dictionary to JSON
    json_data = ujson.dumps(memory_info_dict)
    
    # Send the JSON data over UART
    uart.write(json_data)

def flash_led(led_pin, duration=0.1):
    # Flash the LED for a specified duration
    led_pin.value(1)  # Turn on the LED
    time.sleep(duration)
    led_pin.value(0)  # Turn off the LED

def main():
    uart = machine.UART(1, baudrate=115200, tx=17)  # Change tx pin as per your ESP32 board
    led_pin = machine.Pin(2, machine.Pin.OUT)  # Onboard LED pin, change as needed

    # Example dictionary
    example_dict = {
        1: {
            "data": {
                "start_index": 0,
                "stop_index": 5,
                "operation_code": 1
            }
        },
        2: {
            "data": {
                "start_index": 2,
                "stop_index": 7,
                "operation_code": 2
            }
        },
        3: {
            "data": {
                "start_index": 4,
                "stop_index": 9,
                "operation_code": 0
            }
        },
        4: {
            "data": {
                "start_index": 6,
                "stop_index": 11,
                "operation_code": 3,
                "code": "print('Custom code execution')"
            }
        }
    }

    while True:
        # Sending the entire dictionary
        flash_led(led_pin)  # Flash the LED when sending data
        send_memory_info(uart, example_dict)
        time.sleep(1)

if __name__ == "__main__":
    main()
