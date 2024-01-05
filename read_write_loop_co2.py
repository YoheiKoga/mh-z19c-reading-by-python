import serial
import time

# setting serial port name
# serial_port = "/dev/tty.usbserial-AI03CNY6" 
serial_port = "/dev/tty.usbserial-B001BTPZ" 

baud_rate = 9600
byte_size = 8
parity = 'N'
stop_bits = 1
timeout = None
# xonxoff = False
# rtcts = False
# dsrdtr = False


ser = serial.Serial(port=serial_port, baudrate=baud_rate, bytesize=byte_size, parity=parity, stopbits=stop_bits, timeout=timeout,)

def read_co2_concentration():
    try:
        # send "Read CO2" command
        command_data = bytes([0xFF,0x01,0x86,0x00,0x00, 0x00, 0x00, 0x00, 0x79])
        ser.write(command_data)

        # read "Return Value (CO2 concentration)"
        data = ser.read(9)
        # print("data[2]", data[2])
        # print("data[3]", data[3])
        # print("data[4]", data[4])
        # print("data[5]", data[5])
        # print("data[6]", data[6])
        # print("data[7]", data[7])
        # print("data[8]", data[8])

        # show CO2 concentration
        print(f"=== send data ===")
        print(f"send: {command_data}")
        print(f"=== read data ===")
        print(f"data: {data}")
        print(f"data[2] {data[2]}")
        print(f"data[3] {data[3]}")
        print(f"CO2 Concentration {data[2]*256 + data[3]} ppm")
        print(f"=== === ===")
        print(f"")
        
        
    except Exception as e:
        print(f"Error reading data: {e}")

if __name__ == "__main__":
    try:
        while True:
            read_co2_concentration()
            time.sleep(2)  # 必要に応じて調整
    except KeyboardInterrupt:
        print("プログラムを終了します")
        ser.close()
