
## Overview

The MicroBlaze Code Execution System is specifically designed to integrate seamlessly into a highly parallel memory management system. It facilitates the remote execution of code files on a multitude of MicroBlaze microprocessors. This system allows users to dispatch code files over UART to numerous MicroBlaze devices, each executing the received code and responding with a 16-bit ready flag, device ID, readiness information, and an error flag if any issues arise. This capability is allow efficient coordination of parallel memory management tasks for larger arrays of parallel SISE processors.
(Single Instruction Single execution)

## System Components

### 1. MicroBlaze Microprocessors

Each MicroBlaze microprocessor serves as a processing node within a highly parallel memory management system. Configured to handle code execution, these microprocessors receive code files over UART in order to execute operations on a local memory domain.

### 2. Code Sender (Host System)

The Code Sender component, residing on the host system, is a c-python program running on the is responsible for distributing code files to MicroBlaze devices over UART. This functionality empowers the parallel execution of tasks within the memory management system. 

This system will be a ARM processor running a lightweight linux distribution and standard full featured python.

## Workflow

1. **Code Preparation:**
   - Users prepare code files tailored for highly parallel memory management tasks.

2. **Code Distribution:**
   - The Code Sender on the host system dispatches code files over UART to a multitude of MicroBlaze devices.

3. **Parallel Code Execution:**
   - MicroBlaze devices receive and execute the code concurrently, allowing highly parallelized computation within the memory management system.
   - This system will use a single to many UART communication standard such as RS-432

4. **Response Format:**
   - MicroBlaze responses include:
     - **Ready Flag (16-bit):** Signifies completion of parallel code execution.
	    - **Device ID:** Identifies the individual MicroBlaze device the first (8-bits).
	    - **State Information:** Conveys readiness details using a single Unicode char (8-bits).
		     - **Error Flag:** Indicates issues encountered during parallel code execution represented as ('E').
		     - **Busy Flag:** Indicated with Unicode ('B') represents that the MicroBlaze is currently executing a operation
		     - Ready Flag:  Indicated with Unicode ('R') represents that the MicroBlaze is Ready to receive a new operation instruction

![[PXL_20240114_015649303.jpg]]

5. **Result Handling:**
   - The host system aggregates responses, allowing for comprehensive monitoring and control of parallel tasks. 
   - Error flags trigger corrective actions within the highly parallel memory management system.

## Example Interaction

- The host system initiates parallel code execution tasks by dispatching code files to MicroBlaze devices.
- MicroBlaze devices execute tasks concurrently, providing readiness information and error flags in case of issues.
- The host system orchestrates parallel tasks based on responses, ensuring efficient memory management.

# Proof-of-Concept System Description

## Introduction

Memory management in embedded systems often involves coordination between multiple devices to efficiently utilize shared resources. This proof-of-concept system aims to demonstrate a distributed memory management approach, leveraging dictionaries to store and organize memory-related information.

## System Architecture
The proof of concept was simulated with a ESP-32 micro-controller connected to a computer using their UART0 connected to USB to software serial UART for debug and behavior observation on a development computer .
### Sender
- Generates memory management commands in the form of Python code snippets.
- Utilizes UART communication to transmit commands to the receiver.
### Sender Code (`uart_sender.py`):
```python
import machine
import ujson
import time

uart = machine.UART(1, baudrate=115200, tx=17)  #init ESP32 board UART 2

memory_info_dict = {
    1: {"start_index": 0, "stop_index": 5, "operation_code": 1},
    2: {"start_index": 2, "stop_index": 7, "operation_code": 2},
}

while True:
    # Serialize the dictionary to JSON
    json_data = ''*[2000] #creates a 2000 charicter buffer for sending an receving over uart
    json_data = ujson.dumps(memory_info_dict)
    
    # Send the JSON data over UART
    uart.write(json_data)
    
    time.sleep(1)

```

### Receiver
- Listens for incoming UART communication.
- Processes received commands using the `exec` keyword in upython.
- Utilizes dictionaries to store and retrieve memory management information targeted to specific device IDs.
## Receiver code (`uart_receve_exec.py`):

``` Python
import machine
import ujson
import time

#init UART
uart = machine.UART(1, baudrate=115200, rx=16)  

#
def manage_memory(data):
    print("Received memory information:", data)

    try:
        # Deserialize the JSON data back into a dictionary
        received_memory_info_dict = ujson.loads(data)
        
        # Process the received memory information as needed
        for device_id, info in received_memory_info_dict.items():
            print(f"Device ID: {device_id}, Info: {info}")
            # Implement logic to handle the received memory information
    except Exception as e:
        print("Error processing received data:", e)

while True:
    if uart.any():
        data_received = uart.read(uart.any())
        received_data = data_received.decode('utf-8').strip()
        print("Received data:", received_data)

        # Execute the received data using the manage_memory function
        manage_memory(received_data)
        
    time.sleep(1)

```

### Memory Management Dictionary

The system is the memory management dictionary, where information for operations on each device ID is stored in as shown below.

- **Structure:**
  ```python
  memory_info_dict = {
      0: {"start_index": 0, "stop_index": 5, "operation_code": 1,"data":[0]*(self.stop_index-self.start_index)},
      1: {"start_index": 2, "stop_index": 7, "operation_code": 2},
      3: {"operation_code": 3, "Code":"**** Some Code ****"},
      4:{"operation_code": 0}
      # More device IDs and their information can be added to for real operation
  }
```

**Components:**

- **`start_index` and `stop_index`:**
    - Indicate the range of memory indices relevant to the device.
- **`operation_code`:**
    - An integer code representing the type of memory operation to be performed.
	    - opcode 0 is a no-op
	    - opcode 1 corresponds to delete and replace
	    - opcode 2 corresponds to copy and send
	    - opcode 3 corresponds to a custom operation that will be stored as a string attached to the dictionary

future refactoring can be designed to use arrays to lower performance and memory

For the purpose of this test the behavior is simply printed to the ESP 32 REPL

## Libraries used:
1. **machine:**
    
    - **Description:** This library is specific to MicroPython, a Python implementation for microcontrollers and constrained systems. The `machine` module provides access to hardware-specific functionalities on microcontrollers, such as UART communication.
2. **ujson:**
    
    - **Description:** The `ujson` module is a MicroPython-specific module for handling JSON (JavaScript Object Notation) data. It provides functions for encoding Python objects into JSON format (`ujson.dumps`) and decoding JSON data into Python objects (`ujson.loads`).
3. **time:**
    
    - **Description:** The `time` module provides various time-related functions. In the context of the provided code, it is used for introducing delays (`time.sleep`) between sending data over UART.

## Issues and Developmental trouble

#### UART communication issues:
	- USB Serial to ESP32 UART communication issues

