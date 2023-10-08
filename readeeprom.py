import serial

# Define the Arduino's serial port (change this to match your Arduino's port)
#arduino_port = '/dev/ttyUSB0'  # Linux
arduino_port = 'COM5'  # Windows, replace 'x' with the appropriate COM port number

try:
    arduino = serial.Serial(arduino_port, 9600, timeout=1)
    arduino.write(b'R')  # Send the 'R' command to read EEPROM

    # Read and display the response from Arduino (EEPROM data)
    eeprom_data = arduino.read()
    print(f"EEPROM Data: {eeprom_data}")

    arduino.close()

except serial.SerialException:
    print("Failed to open the Arduino serial port.")
