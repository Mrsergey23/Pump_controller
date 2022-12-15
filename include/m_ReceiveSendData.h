#ifndef __M_RECEIVESENDDATA_H___
#define __M_RECEIVESENDDATA_H___
#include "Arduino.h"

extern uint16_t data[10]; 

void m_ReceiveData();
void m_SendData(int key, int* data, int amount);
#endif //__M_RECEIVESENDDATA_H___