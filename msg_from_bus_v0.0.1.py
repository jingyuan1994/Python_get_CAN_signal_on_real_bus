## Receive CAN and draw the animation plot
# Version: 0.0.1
# Author: Jingyuan Jiang
# E-mail: jingyuan.jiang@faw-vw.com
# Orgnization: FAW-Volkswagen E-Antrieb
# Project: Get special CAN signals from real bus
# Date: 2020-06-01
# Description: This script could be used as reference for reading the CAN signal on real bus by every 0.2s
#              via Vector CANoe


## import the library
import can
import cantools
import csv
import time
import threading

## SETUP and definations
# load dbc (ACAN)
dbACAN = cantools.database.load_file('DBC_ACAN.dbc')

# Set ID
ID1 = 0x1A
ID2 = 0x1B
ID3 = 0x1C

# interfaces setup
bus1 = can.interface.Bus(bustype='vector', app_name='CANoe', can_filters=[{"can_id": ID1, "can_mask": 0xFFF, "extended": False}], channel=1, bitrate=500000, rx_queue_size=10000, receive_own_messages=False)
bus2 = can.interface.Bus(bustype='vector', app_name='CANoe', can_filters=[{"can_id": ID2, "can_mask": 0xFFF, "extended": False}], channel=1, bitrate=500000, rx_queue_size=10000, receive_own_messages=False)
bus3 = can.interface.Bus(bustype='vector', app_name='CANoe', can_filters=[{"can_id": ID3, "can_mask": 0xFFF, "extended": False}], channel=1, bitrate=500000, rx_queue_size=10000, receive_own_messages=False)

## function for reading the signal
def ReadCAN():
    global SPEED, REL_T, VCU_T
    global recvMsg1, recvMsg2, recvMsg3
    global Dmsg1, Dmsg2, Dmsg3
    global timer

    # receive msgs from interfaces
    recvMsg1 = bus1.recv(timeout=None)
    recvMsg2 = bus2.recv(timeout=None)
    recvMsg3 = bus3.recv(timeout=None)

    # message decoding
    Dmsg1 = dbACAN.decode_message('ES1', recvMsg1.data)
    Dmsg2 = dbACAN.decode_message('EM1', recvMsg2.data)
    Dmsg3 = dbACAN.decode_message('Br01', recvMsg3.data)

    # get signal value by name
    SPEED = Dmsg1['ESignal']
    REL_T = Dmsg2['EM']
    VCU_T = Dmsg3['EB']

    # print and save
    print(SPEED,REL_T,VCU_T)
    with open("test.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([SPEED,REL_T,VCU_T])
        csvfile.close()

    # 0.2s repeat
    timer = threading.Timer(0.2, ReadCAN)
    timer.start()

# main
ReadCAN()