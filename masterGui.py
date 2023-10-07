import sys
import time
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

# Define the Arduino Mega's serial port (change this to match your Arduino's port)
# arduino_port = '/dev/ttyUSB0'  # Linux
arduino_port = 'COM5'  # Windows, replace 'x' with the appropriate COM port number

# Create a serial connection to the Arduino
arduino = serial.Serial(arduino_port, baudrate=9600, timeout=1)

def generate_unique_code(name, nic, age, slave_no, code_length=20):
    # Create a unique alphanumeric code with a fixed length (20 characters)
    timestamp = int(time.time())
    code = f"{name[:2]}{nic[-2:]}{str(age)[:2]}{str(slave_no)[:2]}{timestamp}"
    
    # Ensure the code is exactly 20 characters by padding with zeros if needed
    if len(code) < code_length:
        code += '0' * (code_length - len(code))
    
    return code[:code_length]

def generate_code_button_clicked():
    name = name_input.text()
    nic = nic_input.text()
    age = age_input.text()
    slave_no = slave_input.text()

    alphanumeric_code = generate_unique_code(name, nic, age, slave_no, code_length=20)
    result_label.setText(f"Unique Alphanumeric Code: {alphanumeric_code}")
    
    # Disable the "Generate" button after generating the code
    generate_button.setEnabled(False)
    # Enable the "Add New Information" and "Save" buttons
    add_info_button.setEnabled(True)
    save_button.setEnabled(True)
    
    # Store the generated code in a global variable for later use
    global current_code
    current_code = alphanumeric_code

def reset_form():
    # Clear input fields and labels, and enable the "Generate" button
    name_input.clear()
    nic_input.clear()
    age_input.clear()
    slave_input.clear()
    result_label.clear()
    generate_button.setEnabled(True)
    add_info_button.setEnabled(False)
    save_button.setEnabled(False)

def save_to_arduino():
    global current_code
    if current_code:
        # Send the code to the Arduino over the serial connection
        arduino.write(current_code.encode())
        # Clear the current code variable
        current_code = ""
        # Reset the form
        reset_form()
    
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Fixed-Length (20) Unique Alphanumeric Code Generator')

name_label = QLabel('Name:')
name_input = QLineEdit()

nic_label = QLabel('NIC No:')
nic_input = QLineEdit()

age_label = QLabel('Age:')
age_input = QLineEdit()

slave_label = QLabel('Slave No:')
slave_input = QLineEdit()

generate_button = QPushButton('Generate Unique Alphanumeric Code')
generate_button.clicked.connect(generate_code_button_clicked)

result_label = QLabel('Unique Alphanumeric Code:')

add_info_button = QPushButton('Add New Information')
add_info_button.setEnabled(False)
add_info_button.clicked.connect(reset_form)

save_button = QPushButton('Save to Arduino')
save_button.setEnabled(False)
save_button.clicked.connect(save_to_arduino)

input_layout = QVBoxLayout()
input_layout.addWidget(name_label)
input_layout.addWidget(name_input)
input_layout.addWidget(nic_label)
input_layout.addWidget(nic_input)
input_layout.addWidget(age_label)
input_layout.addWidget(age_input)
input_layout.addWidget(slave_label)
input_layout.addWidget(slave_input)
input_layout.addWidget(generate_button)
input_layout.addWidget(result_label)
input_layout.addWidget(add_info_button)
input_layout.addWidget(save_button)

button_layout = QHBoxLayout()
button_layout.addLayout(input_layout)

window.setLayout(button_layout)
window.show()

sys.exit(app.exec_())
