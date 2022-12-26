import serial
import time
ser = serial.Serial('/dev/cu.usbmodem142101', timeout=1)
time.sleep(3)

def getHeightData(ser):
    ser.write(b"send\n")
    height = ser.readline()
    duration = ser.readline()
    return height

def turnAngle(ser, angle):
    ser.write(b"turn\n")
    ser.write(str(angle).encode() + b"\n")

def resetAngle(ser):
    ser.write(b"reset\n")

def giveSugar(ser):
    ser.write(b"sugar\n")



# while True:
#     resetAngle(ser)

# resetAngle(ser)


turnAngle(ser, 30)
