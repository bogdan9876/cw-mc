import serial


class SerialConnection:
    def __init__(self, port="COM3", baudrate=9600):
        self.ser = serial.Serial(port, baudrate)

    def send_command(self, command: bytes):
        self.ser.write(command)

    def read_data(self):
        data = self.ser.readline().decode().strip()
        return data
