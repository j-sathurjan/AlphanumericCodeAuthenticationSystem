import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

# Define the Arduino UNO's serial port (change this to match your Arduino's port)
uno_port = '/dev/ttyACM0'  # Linux
# uno_port = 'COMx'  # Windows, replace 'x' with the appropriate COM port number

# Create a serial connection to the Arduino UNO
uno = serial.Serial(uno_port, baudrate=9600, timeout=1)

def verify_code():
    # Get the user-entered code from the input field
    user_code = code_input.text()

    # Send the user code to the Arduino UNO using serial communication
    uno.write(user_code.encode())

    # Read the response from the Arduino UNO
    response = uno.readline().decode().strip()

    if response == "Match":
        result_label.setText("Code Verified: Match")
    else:
        result_label.setText("Code Verification Failed: No Match")

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Alphanumeric Code Verification')

code_label = QLabel('Enter Alphanumeric Code:')
code_input = QLineEdit()

verify_button = QPushButton('Verify Code')
verify_button.clicked.connect(verify_code)

result_label = QLabel('Verification Result:')

layout = QVBoxLayout()
layout.addWidget(code_label)
layout.addWidget(code_input)
layout.addWidget(verify_button)
layout.addWidget(result_label)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
