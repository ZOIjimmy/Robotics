import pyfirmata
from pyfirmata import util
# from pyfirmata.util import ping_time_to_distance
import time

board = pyfirmata.Arduino('/dev/tty.usbmodem14101')

iterator = util.Iterator(board)
iterator.start()

trigpin = board.get_pin('d:12:o')
echopin= board.get_pin('d:13:i')

while True:
    trigpin.write(0)
    time.sleep(1/1000000.0)
    trigpin.write(1)
    time.sleep(11/1000000.0)
    trigpin.write(0)

    pulse = False
    for i in range(int(1e6)):
        # print(echopin.read())
        if not pulse and echopin.read() == 1:
            start = time.time_ns()
            pulse = not pulse
        if pulse and echopin.read() == 0:
            end = time.time_ns()
            break
        # time.sleep(1/1e9)


    # while echopin.read() == 0:
    #     pass
    # start = time.perf_counter_ns()
    # while echopin.read() == 1:
    #     pass
    # end = time.perf_counter_ns()
    
    # duration = echopin.ping()

    print(start, end)
    duration = (end - start) / 1000
    distance = (duration / 2.0) * 340 * 100 / 1000000
    print(duration, "us")
    print(distance, "cm")
    time.sleep(0.5)