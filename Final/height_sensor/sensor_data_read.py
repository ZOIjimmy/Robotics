import serial
ser = serial.Serial('/dev/cu.usbmodem14101', timeout=1)
ser.readline()

for i in range(50):
    line = ser.readline()   # read a byte
    print(line)