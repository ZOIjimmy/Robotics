# import serial
import time
# ser = serial.Serial('/dev/cu.usbmodem141201', timeout=1)
# time.sleep(3)

def getHeightData(ser):
    ser.write(b"send\n")
    height = ser.readline()
    duration = ser.readline()
    return height

def turnAngle(ser, angle):
    print(str(angle).encode())
    ser.write(str(angle).encode())
    ser.write(b"\n")
    return 2

def resetTurnAngle(ser):
    ser.write(b"reset")
    ser.write(b"\n")
    return 1

def giveSugar(ser):
    ser.write(b"sugar\n")



# while True:
#     resetAngle(ser)

# resetAngle(ser)


# turnAngle(ser, 30)
