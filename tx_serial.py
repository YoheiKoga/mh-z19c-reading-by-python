import serial
import time

# set serial port
serial_port = "/dev/tty.usbserial-xxxxxxxx" # please fill your own serialport information 
baud_rate = 9600
byte_size = 8
parity = 'N'
stop_bits = 1
timeout = None
# xonxoff = False
# rtcts = False
# dsrdtr = False

ser = serial.Serial(port=serial_port, baudrate=baud_rate, bytesize=byte_size, parity=parity, stopbits=stop_bits, timeout=timeout,)



try:
    while True:
        # command set: Read CO2 concentration
        command_data = bytes([0xFF,0x01,0x86,0x00,0x00, 0x00, 0x00, 0x00, 0x79])

        # send command
        ser.write(command_data)
        print(f"Sent command: {command_data}")
        time.sleep(1)
except Exception as e:
    print(f"Error: {e}")
finally:
    # serial port close
    ser.close()

