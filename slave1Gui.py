import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame
from serial.tools import list_ports
from PyQt5.QtCore import QTimer

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
        connect_button.setText('Connect to Arduino')
        connect_button.setEnabled(True)
    # Get the selected serial port from the dropdown
    selected_port = port_combobox.currentText()
    try:
        # Attempt to create a new connection to the Arduino
        uno = serial.Serial(selected_port, baudrate=115200, timeout=1)
        connect_button.setText('Connected')
        connect_button.setEnabled(False)
        connect_button.hide()
        disconnect_button.show()
        port_combobox.setEnabled(False)
        scan_button.setEnabled(False)
    except Exception as e:
        result_label.setText(f'Failed to connect: {"Arduino"}')

def disconnect_from_arduino():
    global uno
    if uno and uno.isOpen():
        uno.close()
        connect_button.setText('Connect to Arduino')
        connect_button.setEnabled(True)
        connect_button.show()
        disconnect_button.hide()
        port_combobox.setEnabled(True)
        scan_button.setEnabled(True)

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

    if response == "Gate is open":
        result_label.setText("Code Verified: Match, Gate is open.")
        verify_button.setEnabled(False)
        QTimer.singleShot(3000, update_result_label_to_closed)
    else:
        result_label.setText("Code Verification Failed: No Match, Gate is closed.")
        
def update_result_label_to_closed():
    result_label.setText("Gate is closed")
    verify_button.setEnabled(True)
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Slave GUI')

port_label = QLabel('Select Arduino COM Port:')
port_combobox = QComboBox()

scan_button = QPushButton('Scan Ports')
scan_button.clicked.connect(scan_ports)

connect_button = QPushButton('Connect to Arduino')
connect_button.clicked.connect(connect_to_arduino)

disconnect_button = QPushButton('Disconnect')
disconnect_button.clicked.connect(disconnect_from_arduino)

# Layout for Port Selection, Scan Port, Connect Arduino, and Disconnect Arduino in the same line
button_layout = QHBoxLayout()
button_layout.addWidget(port_label)
button_layout.addWidget(port_combobox)
button_layout.addWidget(scan_button)
button_layout.addWidget(connect_button)
button_layout.addWidget(disconnect_button)
disconnect_button.hide()

# Horizontal Line Separator
line = QFrame()
line.setFrameShape(QFrame.HLine)
line.setFrameShadow(QFrame.Sunken)

# Input Alphanumeric Code Layout
code_layout = QVBoxLayout()

code_label = QLabel('Enter Alphanumeric Code:')
code_input = QLineEdit()

verify_button = QPushButton('Verify Code')
verify_button.clicked.connect(verify_code)

result_label = QLabel('Verification Result:')

code_layout.addWidget(line)  # Add the separator line
code_layout.addWidget(code_label)
code_layout.addWidget(code_input)
code_layout.addWidget(verify_button)
code_layout.addWidget(result_label)

# Main Layout
main_layout = QVBoxLayout()
main_layout.addLayout(button_layout)
main_layout.addLayout(code_layout)

window.setLayout(main_layout)
window.setFixedSize(450, 200)
window.show()

sys.exit(app.exec_())
