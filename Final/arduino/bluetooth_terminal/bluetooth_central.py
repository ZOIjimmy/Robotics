# import serial
# BTserial = serial.Serial('/dev/ttys003', 9600)
# print(BTserial.name)
# BTserial.flushInput()

# print(BTserial.writable())
# BTserial.write(b'12345;')

# print(BTserial.readline())
# BTserial.close()




# (target)sudo apt install libglib2.0-dev 
# (target)sudo pip install bluepy

# from bluepy.btle import Peripheral, UUID
# from bluepy.btle import Scanner, DefaultDelegate

# class ScanDelegate(DefaultDelegate):
#     def __init__(self):
#         DefaultDelegate.__init__(self)
#     def handleDiscovery(self, dev, isNewDev, isNewData):
#         if isNewDev:
#             print ("Discovered device", dev.addr)
#         elif isNewData:
#             print ("Received new data from", dev.addr)
# scanner = Scanner().withDelegate(ScanDelegate())
# devices = scanner.scan(10.0)
# n=0
# addr = []
# for dev in devices:
#     print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr,dev.addrType, dev.rssi))
#     addr.append(dev.addr)
#     n += 1
#     for (adtype, desc, value) in dev.getScanData():
#         print (" %s = %s" % (desc, value))
# number = input('Enter your device number: ')
# print ('Device', number)
# num = int(number)
# print (addr[num])
# #
# print ("Connecting...")
# dev = Peripheral(addr[num], 'random')
# #
# print ("Services...")
# for svc in dev.services:
#     print (str(svc))
# #
# try:
#     testService = dev.getServiceByUUID(UUID(0xfff0))
#     for ch in testService.getCharacteristics():
#         print (str(ch))
# #
#     desList = dev.getDescriptors()
#     for des in desList:
#         if des.uuid == UUID(0x2902):
#             print("Value before write: " + str(des.read()))
#             des.write(b'\x02\x00')
#             print("Value after write: " + str(des.read()))
# #
# finally:
#     dev.disconnect()




# simple inquiry example
# import bluetooth

# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# print("Found {} devices.".format(len(nearby_devices)))

# for addr, name in nearby_devices:
#     print("  {} - {}".format(addr, name))