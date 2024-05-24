#this file is to send commands to the esp32 
#esp32 is precompiled with another script for recieving 


import serial
import time

def serialSend(command):
    # Define the serial port and baud rate
    serial_port = '/dev/ttyUSB0'  # Update this with the appropriate serial port
    baud_rate = 115200  # Update this with the baud rate configured on your device

    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate)

    # Wait for the serial port to initialize
    # time.sleep(0.5)

    ser.write(command)
    # Close the serial port
    ser.close()