This code is mostly functional and more representative of behavior similar to that I would expect to see between the arm core and the Micro-Blaze green cores.

This code uses dictionaries indexed by device id and opcode to maniplulate an array of values. there are 4 types of opcodes:
	-0: no operation
	-1: read and send over UART
		- dictionary will contain array start and stop indicies for op
	-2: delete/write
		-dictionary will contain array start stop indicies and data for op
	-3: execute arbitrary upy code
		-dictionary will contain string to be executed
For more detales on dictionary structire see the example dictionary in the   esp_send_test.py file.

The current archetecture of this code is desinged to have a single device cycle through multible device ids to simulate multiple devices reading the same uart tx pin and outputing data over the REPL (uart0 serial-> dev/tty/USB0)

This code is mostly funcitonal but still has wrinkles that need to be ironed out but serves as a vision for how a memory read write system could work

TODO:

- implemnt recive device state flags (see main research doc)
- Fix error with ocasional dictionary uart buffer overflow
- Simplify ditionary archetecture
