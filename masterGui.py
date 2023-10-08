import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout

# Global variable to hold the Arduino connection
arduino = None

def generate_alphanumeric_code(name, nic, gate):
    # Extract the required portions of the input data
    gate_code = str(gate)
    nic_last_10_digits = nic[-10:]
    name_first_5_chars = name[:5]

    # Concatenate the portions to create a 16-character code
    alphanumeric_code = gate_code + nic_last_10_digits + name_first_5_chars

    # Ensure the code is exactly 16 characters by padding with zeros if needed
    if len(alphanumeric_code) < 16:
        alphanumeric_code += '0' * (16 - len(alphanumeric_code))

    return alphanumeric_code

def scan_ports():
    # Get a list of available COM ports
    available_ports = [port.device for port in serial.tools.list_ports.comports()]
    port_combo.clear()
    port_combo.addItems(available_ports)

def connect_to_arduino():
    global arduino  # Use the global arduino variable

    # Get the selected COM port
    selected_port = port_combo.currentText()

    try:
        # Create a serial connection to the selected Arduino
        arduino = serial.Serial(selected_port, baudrate=9600, timeout=1)
        result_label.setText(f"Connected to Arduino on {selected_port}")
    except serial.SerialException:
        result_label.setText(f"Failed to connect to Arduino on {selected_port}")

def send_code_to_arduino():
    if arduino is None:
        result_label.setText("Arduino not connected. Please connect first.")
        return

    # Get the input values from the user
    name = name_input.text()
    nic = nic_input.text()
    gate = gate_combo.currentText()

    # Generate the alphanumeric code
    alphanumeric_code = generate_alphanumeric_code(name, nic, gate)

    # Send the code to the Arduino
    arduino.write(alphanumeric_code.encode())
    
    result_label.setText(f"Your gate entering code: {alphanumeric_code}")

def retrieve_list_from_arduino():
    if arduino is None:
        result_label.setText("Arduino not connected. Please connect first.")
        return

    # Send the "get_list" command to Arduino
    arduino.write("allKeysSlave2\n".encode())

    # Read the response from Arduino (the list of data)
    response = arduino.readline().decode().strip()

    # Print the response to the console
    print(f'Response from Arduino: {response}')

    # Create a new UI to display the retrieved list
    list_window = QWidget()
    list_window.setWindowTitle('Retrieved List')
    list_layout = QVBoxLayout()

    list_label = QLabel(f'Retrieved List:\n{response}')
    list_layout.addWidget(list_label)

    list_window.setLayout(list_layout)
    list_window.show()

def update_register_button_state():
    # Check if Name and NIC No fields are empty, then enable/disable the button
    name = name_input.text()
    nic = nic_input.text()
    is_valid = len(name) >= 5 and len(nic) >= 10
    generate_button.setEnabled(is_valid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Alphanumeric Code Generator and Arduino Sender')

    # Create a top-level layout for the port selection
    port_layout = QHBoxLayout()

    port_label = QLabel('Select Arduino COM Port:')
    port_combo = QComboBox()
    scan_button = QPushButton('Scan Ports')
    scan_button.clicked.connect(scan_ports)
    connect_button = QPushButton('Connect to Arduino')
    connect_button.clicked.connect(connect_to_arduino)

    port_layout.addWidget(port_label)
    port_layout.addWidget(port_combo)
    port_layout.addWidget(scan_button)
    port_layout.addWidget(connect_button)

    # Create a layout for the input fields and buttons
    input_layout = QVBoxLayout()

    name_label = QLabel('Name:')
    name_input = QLineEdit()
    name_input.textChanged.connect(update_register_button_state)  # Connect the textChanged signal

    nic_label = QLabel('NIC No:')
    nic_input = QLineEdit()
    nic_input.textChanged.connect(update_register_button_state)  # Connect the textChanged signal

    # Create a grid layout for "Gate No" label and dropdown
    gate_grid_layout = QGridLayout()
    gate_label = QLabel('Gate No:')
    gate_combo = QComboBox()
    gate_combo.addItems(['1', '2'])
    gate_grid_layout.addWidget(gate_label, 0, 0)  # Row 0, Column 0
    gate_grid_layout.addWidget(gate_combo, 0, 1)   # Row 0, Column 1

    generate_button = QPushButton('Register User')
    generate_button.setEnabled(False)  # Initially disable the button
    generate_button.clicked.connect(send_code_to_arduino)

    # Create a button to retrieve the list
    retrieve_list_button = QPushButton('Retrieve List')
    retrieve_list_button.setEnabled(True)  # Initially enable the button
    retrieve_list_button.clicked.connect(retrieve_list_from_arduino)

    result_label = QLabel('')

    input_layout.addWidget(name_label)
    input_layout.addWidget(name_input)
    input_layout.addWidget(nic_label)
    input_layout.addWidget(nic_input)
    input_layout.addLayout(gate_grid_layout)  # Add the gate_grid_layout
    input_layout.addWidget(generate_button)
    input_layout.addWidget(retrieve_list_button)  # Add the retrieve_list_button

    # Create a layout for the result label
    result_layout = QVBoxLayout()
    result_layout.addWidget(result_label)

    # Create a main layout to arrange the top-level and input layouts
    main_layout = QVBoxLayout()
    main_layout.addLayout(port_layout)
    main_layout.addLayout(input_layout)
    main_layout.addLayout(result_layout)

    window.setLayout(main_layout)
    window.show()

    sys.exit(app.exec_())
