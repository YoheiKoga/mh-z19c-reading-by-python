import PySimpleGUI as sg
import datetime
import serial
from serial.tools import list_ports
import time

# baudrate
LIST_BAUDRATE = [
    '300 bps',
    '1200 bps',
    '2400 bps',
    '4800 bps',
    '9600 bps',
    '19200 bps',
    '38400 bps',
    '57600 bps',
    '74800 bps',
    '115200 bps'
]

# port list
def list_port():
    ports = list_ports.comports()
    devices = [info.device for info in ports]

    # print(devices)

    return devices

# open port
def open_port(port, baudrate):
    ser = serial.Serial()
    ser.baudrate = int(baudrate[0:-4])
    ser.timeout = 0.01
    ser.port = port

    try:
        ser.open()
        return ser
    except:
        print("error when opening serial")
        return None


# print to output area
def printOut(s, sep, scroll, timestamp):
    if timestamp==True:
        now = datetime.datetime.now().strftime('%H:%M:%S.%f')
        sg.cprint(now[0:-3]+sep+s, end="", autoscroll=scroll)
    else:
        sg.cprint(s,end="", autoscroll=scroll)

# serial monitor
com_list = list_port()

layout = [
    [
        # sg.Input('', size=(10,1), font=('MS Gothic', 10), expand_x=True, key='-IN-'),
        sg.Button('Start', bind_return_key=True, key='-START-')
    ],
    [
        sg.Multiline('', size=(80, 30), font=('MS Gothic', 10), expand_x=True, expand_y=True, key='-OUT-')
    ],
    [
        sg.Checkbox('AutoScroll', default=True, key='-AutoScroll-'),
        sg.Checkbox('Timestamp', default=False, key='-Timestamp-'),
        sg.Stretch(),
        # sg.Combo(values=list(DICT_NEWLINE.keys()), default_value='CR+LF', readonly=True, key='-newline-'),
        sg.Combo(values=com_list, default_value=com_list[0], enable_events=True, readonly=True, key='-port-'),
        sg.Combo(values=LIST_BAUDRATE, default_value='9600 bps', enable_events=True, readonly=True, key='-baudrate-'),
        sg.Button('Clear', key='-CLEAR-')
    ]
]

window = sg.Window('MH-Z19', layout, resizable=True, return_keyboard_events=True)
sg.cprint_set_output_destination(window, '-OUT-')

ser = open_port(window['-port-'].DefaultValue, window['-baudrate-'].DefaultValue)

while True:
    event, values = window.read(timeout = 2)
    if event == sg.WIN_CLOSED:
        break
    if event == '-START-':
        try:
            print("")
            print("===")
            print("send [0xFF,0x01,0x86,0x00,0x00, 0x00, 0x00, 0x00, 0x79]")
            print("===")
            print("")
            # ser.write(w_data.encode())
            # ser.write(bytes(w_data.encode()))
            ser.write(bytes([0xFF,0x01,0x86,0x00,0x00, 0x00, 0x00, 0x00, 0x79]))

        except KeyboardInterrupt:
            print("program is closed")
            ser.close()

    if event == '-port-' or event == '-baudrate-':
        if ser is not None:
            ser.close()
        ser = open_port(values['-port-'], values['-baudrate-'])
    if event == '-CLEAR-':
        window['-OUT-'].update('')
    
    if ser is not None:
        if ser.is_open:
            while True:
                data = ser.read(9)
                if data == b'':
                    break
                try:
                    # printOut(data.decode(), ' -> ', values['-AutoScroll-'], values['-Timestamp-'])
                    printOut(f"CO2 concentration: {data[2]*256+data[3]} ppm \n", ' -> ', values['-AutoScroll-'], values['-Timestamp-'])
                except:
                    print('Decode Error')

if ser is not None:
    ser.close()

window.close()