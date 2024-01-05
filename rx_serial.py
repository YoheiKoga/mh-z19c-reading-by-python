mport serial
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
    # receive data
    received_data = ser.read(8)
    received_hex = received_data.hex()
    print(f"Received: {received_hex}")
except Exception as e:
    print(f"Error: {e}")
finally:
    # serial port close
    ser.close()


