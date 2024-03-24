import serial
import time
import serial.tools.list_ports

connected = False
pserial = None

def connect_to_macroboard():
    global connected,pserial
    while not connected:
        try:
            macroport = "COM4"
            ports = serial.tools.list_ports.comports()
            print(ports)
            for port, desc, hwid in sorted(ports):
                if hwid.find("USB VID:PID=0001:0001") != -1:
                    macroport = port
            pserial = serial.Serial(macroport, 115200)
        except Exception as e:
            print(e)
            time.sleep(3)
        else:
            connected = True
            print("connected")
            return True

connect_to_macroboard()
pserial.write("003\r".encode())
while True:
    data = pserial.read(1).decode()
    print(data)