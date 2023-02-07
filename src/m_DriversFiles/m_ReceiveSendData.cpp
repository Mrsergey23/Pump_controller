#include "m_ReceiveSendData.h"

void m_ReceiveData()
{
    char str[30];
    int amount = Serial.readBytesUntil(';', str, 30);
    str[amount] = NULL;
    int count = 0;
    char* offset = str;
    while (true)
    {
        data[count++] = atoi(offset);
        offset = strchr(offset, ',');
        if (offset) offset++;
        else break;
    }   
}

// функция для отправки пакета на ПК
void m_SendData(int key, int* data, int amount) {
  Serial.print(key);
  Serial.print(',');
  for (int i = 0; i < amount; i++) 
  {
    Serial.print(data[i]);
    if (i != amount - 1) Serial.print(',');
  }
  Serial.print('\r');
}