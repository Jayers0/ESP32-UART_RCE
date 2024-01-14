# Joshua Ayers blinky test code for ESP32

from machine import Pin
import time

# Define the GPIO pin connected to the LED
led_pin = Pin(2, Pin.OUT)  

# Function to blink the LED
def blink_led():
    while True:
        led_pin.on()   # Turn on the LED
        time.sleep(1)  # Wait for 1 second
        led_pin.off()  # Turn off the LED
        time.sleep(1)  # Wait for 1 second

# Call the blink_led function
blink_led()
