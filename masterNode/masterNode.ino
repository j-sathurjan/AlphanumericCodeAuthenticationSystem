#include <FlashAsEEPROM.h>
#include <FlashStorage.h>


// Create a FlashStorage object to store the alphanumeric code
FlashStorage(alphanumeric_storage, String);

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Your code here...
}

void saveAlphanumericCode(String code) {
  alphanumeric_storage.write(code);
  Serial.println("Alphanumeric code saved to flash memory");
}

String readAlphanumericCode() {
  String code = alphanumeric_storage.read();
  Serial.print("Read Alphanumeric Code from flash memory: ");
  Serial.println(code);
  return code;
}
