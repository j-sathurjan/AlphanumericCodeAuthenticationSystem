#include <SPI.h>
#define MAX_KEYS_LENGTH 50

String codeSlave1[MAX_KEYS_LENGTH] = {"123456789asdfgh1"};
String codeSlave2[MAX_KEYS_LENGTH] = {"123456789asdfgh2"};
int codeSlave1Index = 0;
int codeSlave2Index = 0;

void setup()
{
  SPI.begin();
  pinMode(10, OUTPUT);
  pinMode(52, OUTPUT);
  pinMode(4, OUTPUT);
  Serial.begin(9600);
  Serial.println("master ok");
}

void loop()
{
  if (Serial.available())
  {
    String input = Serial.readStringUntil('\n');
    if (input.substring(0, 12) == "inputSlave1:")
    {
      codeSlave1Index = codeSlave1Index + 1;
      if (codeSlave1Index > MAX_KEYS_LENGTH)
        codeSlave1Index = 0;

      String inputDetails = input.substring(12);
      String string1, string2, string3;

      int firstCommaIndex = inputDetails.indexOf(',');
      int secondCommaIndex = inputDetails.indexOf(',', firstCommaIndex + 1);
      string1 = inputDetails.substring(0, firstCommaIndex);
      string2 = inputDetails.substring(firstCommaIndex + 1, secondCommaIndex);
      string3 = inputDetails.substring(secondCommaIndex + 1);

      if (string1.length() > 9)
      {
        string1 = string1.substring(string1.length() - 10);
        if (string2.length() > 4)
        {
          string2 = string2.substring(0, 5);
          if(string3.length()>1){
            Serial.println("data error");
          }else{
            char ciphertext[16];
            encrypt((string1+string2+string3).c_str(), ciphertext);
            String ciphertextString = ciphertext;
            codeSlave1[codeSlave1Index] = ciphertextString.substring(0,16);
            Serial.println(codeSlave1[codeSlave1Index]);
          }
        }
        else
        {
          Serial.println("data error");
        }
      }
      else
      {
        Serial.println("data error");
      }

      // char plaintext[16];
      // decrypt(ciphertext, plaintext);
      // Serial.print("DC");
      // Serial.println(plaintext);
    }
    else if (input.substring(0, 12) == "inputSlave2:")
    {
      codeSlave2Index = codeSlave2Index + 1;
      if (codeSlave2Index > MAX_KEYS_LENGTH)
        codeSlave2Index = 0;

      String inputDetails = input.substring(12);
      String string1, string2, string3;

      int firstCommaIndex = inputDetails.indexOf(',');
      int secondCommaIndex = inputDetails.indexOf(',', firstCommaIndex + 1);
      string1 = inputDetails.substring(0, firstCommaIndex);
      string2 = inputDetails.substring(firstCommaIndex + 1, secondCommaIndex);
      string3 = inputDetails.substring(secondCommaIndex + 1);

      if (string1.length() > 9)
      {
        string1 = string1.substring(string1.length() - 10);
        if (string2.length() > 4)
        {
          string2 = string2.substring(0, 5);
          if(string3.length() > 1){
            Serial.println("data error : gate");
            Serial.println(string3.length());
          }else{
            char ciphertext[16];
            encrypt((string1+string2+string3).c_str(), ciphertext);
            String ciphertextString = ciphertext;
            codeSlave2[codeSlave2Index] = ciphertextString.substring(0,16);
            Serial.println(codeSlave2[codeSlave2Index]);
          }
        }
        else
        {
          Serial.println("data error : Name");
        }
      }
      else
      {
        Serial.println("data error : NIC");
      }
    }
    else if (input.substring(0, 12) == "allKeysSlave")
    {
      String allKeys = "gate1,";
      for (int i = 0; i < codeSlave1Index + 1; i++)
      {
        allKeys = allKeys + codeSlave1[i] + ",";
      }
      allKeys = allKeys + "gate2,";
      for (int i = 0; i < codeSlave2Index + 1; i++)
      {
        allKeys = allKeys + codeSlave2[i] + ",";
      }
      Serial.println(allKeys);
    }
  }
  checkSlave(10, codeSlave1,codeSlave1Index);
  checkSlave(4, codeSlave2,codeSlave2Index);
}

void checkSlave(int slavePin, String code[], int index)
{
  // Serial.println(slavePin);
  digitalWrite(slavePin, LOW);
  SPI.transfer('a');
  delay(100);
  byte response = SPI.transfer(0x00);
  // Serial.println(response);
  if (response == 'd')
  {
    char data[17];
    for (int i = 0; i < 16; i++)
    {
      SPI.transfer(i + 1);
      delay(10);
      data[i] = SPI.transfer(i + 1);
    }
    data[16] = '\0';

    // Serial.print(slavePin);
    // Serial.print(": ");
    // Serial.println(String(data).substring(0, 16));
    bool codeMatch = false;
    for (int i = 0; i < index + 1; i++)
    {
      if (strncmp(data, code[i].c_str(), 16) == 0)
      {
        codeMatch = true;
        break;
      }
    }
    if (codeMatch)
    {
      // Serial.println("ok");
      SPI.transfer(0x20);
    }
    else
    {
      // Serial.println("not ok");
      SPI.transfer(0x21);
    }
  }
  digitalWrite(slavePin, HIGH);
  delay(100);
}

void encrypt(const char *plaintext, char *ciphertext)
{
  const char *key = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  for (int i = 0; i < 16; i++)
  {
    char c = plaintext[i];
    if (isalnum(c))
    {
      int index = (c - '0') % 62;
      ciphertext[i] = key[index];
    }
    else
    {
      ciphertext[i] = c;
    }
  }
}

void decrypt(char *ciphertext, char *plaintext)
{
  const char *key = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  for (int i = 0; i < 16; i++)
  {
    char c = ciphertext[i];
    if (isalnum(c))
    {
      int index = 0;
      for (int j = 0; j < 62; j++)
      {
        if (key[j] == c)
        {
          index = j;
          break;
        }
      }
      plaintext[i] = '0' + index;
    }
    else
    {
      plaintext[i] = c;
    }
  }
}