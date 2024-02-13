import serial
import time
import struct

# Open a serial port. You may have to change the first parameter
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# If the user closes the program, close the serial port
def signal_handler(sig, frame):
	ser.close()
	sys.exit(0)

# Read a byte from serial as a hex pair
def get_hex():
	return hex(int.from_bytes(ser.read(), byteorder="big"))

# Find the beginning of the data
def block_start():
  while True:
    if get_hex() == hex(0xfa):
      if get_hex() == hex(0xff):
        if get_hex() == hex(0x36):
          if get_hex() == hex(0x0f):
            if get_hex() == hex(0x40):
              if get_hex() == hex(0x20):
                if get_hex() == hex(0x0c):
                  return

# Read in 4 bytes and convert them into a 32 bit float
def get_float():
  hex_string = ""
  hex_string += str(get_hex())[2:].zfill(2)
  hex_string += str(get_hex())[2:].zfill(2)
  hex_string += str(get_hex())[2:].zfill(2)
  hex_string += str(get_hex())[2:].zfill(2)

  byte = bytes.fromhex(hex_string)

  return struct.unpack('!f', byte)[0]
  

# Get each acceleration value and print them
while True:
  block_start()
  x_accel = get_float()
  y_accel = get_float()
  z_accel = get_float()
  print(str(x_accel) + '\t' + str(y_accel) + '\t' + str(z_accel))
