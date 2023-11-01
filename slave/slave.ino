#include <SPI.h>

const int GATE_PIN1 = 3;
const int GATE_PIN2 = 4;

char sendDataKey[16];
String text = "abcd1";
bool isNew = false;
bool isGateOpen = false;

void setup() {
  pinMode(MISO, OUTPUT);  
  pinMode(GATE_PIN1, OUTPUT);
  pinMode(GATE_PIN2, OUTPUT);
  SPCR |= _BV(SPE);       
  SPI.attachInterrupt();  
  Serial.begin(115200);   
  Serial.println("Slave is ready");
  digitalWrite(GATE_PIN1, HIGH);
}

void loop() {
    if (Serial.available()) { 
        String input = Serial.readString(); 
        text = input;
        // Serial.println("input: " + text);
        isNew = true;
    }

    if(isGateOpen) {
      openGate();
    } else {
      // Serial.println("Gate is close");
    }
}

void openGate() {
  Serial.println("Gate is open");
  digitalWrite(GATE_PIN2, HIGH);
  digitalWrite(GATE_PIN1, LOW);
  delay(5000);
  digitalWrite(GATE_PIN2, LOW);
  digitalWrite(GATE_PIN1, HIGH);
  isGateOpen = false;
}

void sendData() {
  SPDR = 'd';
  for (int i = 0; i < 16; i++) {
    sendDataKey[i] = text[i];
  }
  isNew = false;
}

void sendError() {
  SPDR = 'e';
}

void sendKey(byte c) {
  SPDR = sendDataKey[c - 1];
  // Serial.println("sendDataKey[" + String(c - 1) + "] " + String(sendDataKey[c - 1]));
  if(c == 17) {
    for(int i = 0; i < 16; i++) {
      sendDataKey[i] = '0';
    }
  }
}

void handleSPI(byte c) {
  if (c == 'a') {
    if(isNew) {
      sendData();
    } else {
      sendError();
    }
  } else if (c >= 0x01 && c <= 0x17) {
    sendKey(c);
  } else if(c == 0x20){
    isGateOpen = true;
  } else if(c == 0x21){
    isGateOpen = false;
  } else {
    sendError();
  }
}

ISR(SPI_STC_vect) {
  byte c = SPDR; 
  // Serial.println(c);
  handleSPI(c);
}