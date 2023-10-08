#include <EEPROM.h>

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'R') {
      int address = 0;  // EEPROM address to read from
      byte data = EEPROM.read(address);
      Serial.write(data);
    }
  }
}
