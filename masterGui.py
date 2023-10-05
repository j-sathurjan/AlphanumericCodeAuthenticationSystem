import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

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

layout = QVBoxLayout()
layout.addWidget(name_label)
layout.addWidget(name_input)
layout.addWidget(nic_label)
layout.addWidget(nic_input)
layout.addWidget(age_label)
layout.addWidget(age_input)
layout.addWidget(slave_label)
layout.addWidget(slave_input)
layout.addWidget(generate_button)
layout.addWidget(result_label)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
