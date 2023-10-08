import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from serial.tools import list_ports

# Create a serial connection to the Arduino UNO
uno = None  # Initialize as None

def scan_ports():
    # Get a list of available COM ports and update the dropdown
    available_ports = [port.device for port in list_ports.comports()]
    port_combobox.clear()
    port_combobox.addItems(available_ports)

def connect_to_arduino():
    global uno
    # Close the existing connection if it's open
    if uno and uno.isOpen():
        uno.close()
    # Get the selected serial port from the dropdown
    selected_port = port_combobox.currentText()
    try:
        # Attempt to create a new connection to the Arduino
        uno = serial.Serial(selected_port, baudrate=115200, timeout=1)
        connect_button.setText('Connected')
        connect_button.setEnabled(False)
    except Exception as e:
        result_label.setText(f'Failed to connect: {str("please select the port")}')

def verify_code():
    if not uno or not uno.isOpen():
        result_label.setText('Not connected to Arduino')
        return

    # Get the user-entered code from the input field
    user_code = code_input.text()

    # Send the user code to the Arduino UNO using serial communication
    uno.write(user_code.encode())

    # Read the response from the Arduino UNO
    response = uno.readline().decode().strip()
    response = uno.readline().decode().strip()
    print(f'Response from Arduino: {response}')

    if response == "Gate is open":
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

port_combobox = QComboBox()

scan_button = QPushButton('Scan Ports')
scan_button.clicked.connect(scan_ports)

connect_button = QPushButton('Connect to Arduino')
connect_button.clicked.connect(connect_to_arduino)

top_layout = QVBoxLayout()
top_layout.addWidget(code_label)
top_layout.addWidget(code_input)

port_layout = QHBoxLayout()
port_layout.addWidget(port_combobox)
port_layout.addWidget(scan_button)

top_layout.addLayout(port_layout)
top_layout.addWidget(connect_button)

layout = QVBoxLayout()
layout.addLayout(top_layout)
layout.addWidget(verify_button)
layout.addWidget(result_label)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
