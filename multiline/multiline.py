import time
from pathlib import Path

import serial

from multiline.sensors import parse_sensor

class MultiLineIDS:
    """ 
    MultiLineIDS class to instantiate a serial connection to a WTW MultiLine IDS 
    instrument. The code has only been tested on the MultiLine 3630 IDS version.

    The instruments technical manual records no commands that the instrument may
    respond to. The instrument will send the current measurements upon pressing 
    the <PRT> button. Performing a long press <PRT_> causes the dialog for 
    automatic data transmission to appear, where the settings for continuous 
    transmission of measurements at set intervals exist.

    This script assumes the baudrate on the instrument was changed from factory 
    default 4800 to 9600. The reason was to accommodate data transmission
    from three sensors once per second. 
    NB: baudrate on instrument and in this script must 
        match eachother.

    USB/RS232 interface settings from manual:
        Baud rate: 1200 ... 19200
        Handshake: RTS/CTS
        Parity: none
        Data bits: 8
        Stop bits: 1

    Instrument sends data from one sensor per line. Some sensors may send 
    multiple lines (e.g. the dissolved oxygen sensor sends one line for 
    concentration and one for saturation). Some sensors do not include certain 
    parameters (the turbidity sensor does not record temperature). Some sensors
    mix up which data is in which column also.

    Example data read (conductivity):
    Multi 3630 IDS; 19410634;;15.04.2020 11:03:48;34.3E+3;µS/cm;Cond;19.2;°C;Temp;AR;;C = 0.475 1/cm   Tref25   nLF;TetraCon 925; 19411430;
    Example data read (dissolved oxygen):
    Multi 3630 IDS; 19410634;;15.04.2020 11:03:48;8.74;mg/l;Ox;19.4;°C;Temp;AR;;SC-FDO   19391671;;FDO 925; 19411244;
    Multi 3630 IDS; 19410634;;15.04.2020 11:03:48;97.0;%;Ox;19.4;°C;Temp;AR;;SC-FDO   19391671;;FDO 925; 19411244;
    """

    def __init__(self, port = "COM6", callback = None, auto_connect = True):
        self.con = serial.Serial()
        self.con.port = port
        self.con.baudrate = 9600
        self.con.bytesize = serial.EIGHTBITS
        self.con.parity = serial.PARITY_NONE
        self.con.stopbits = serial.STOPBITS_ONE
        self.con.rtscts = True
        self.con.timout = None

        self.callback = callback
        self.auto_connect = auto_connect
        print("MultiLine module instantiated.")

        if self.auto_connect:
            self.connect()

    def connect(self) -> bool:
        print(f"Opening serial connection to MultiLine on {self.con.port}.")
        self.con.open()
        return self.is_open()

    def disconnect(self) -> bool:
        print(f"Closing serial connection to MultiLine on {self.con.port}.")
        self.con.close()
        return not self.is_open()

    def is_open(self) -> bool:
        return self.con.is_open

    def read_instrument(self) -> None:
        buffer = b""

        try:
            while True:
                if self.con.in_waiting > 0:
                    chunk = self.con.read(self.con.in_waiting)
                    buffer += chunk
                if (eol := buffer.find(b"\r\n")) != -1:
                    line = buffer[:eol]
                    buffer = buffer[eol+2:]
                    line = line.decode("cp1252")

                    sensor_csv = line + "\n"
                    sensor_dict = parse_sensor(line)

                    if self.callback:
                        try:
                            self.callback(sensor_csv, sensor_dict)
                        except:
                            pass

        except KeyboardInterrupt:
            if self.auto_connect:
                self.disconnect()
        

