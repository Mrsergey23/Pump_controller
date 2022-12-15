#ifndef _M_ACS712_H__
#define _M_ACS712_H__
#include <Arduino.h>

extern int16_t A_zero_level;   //  Optional zero level, because sensor is two polar, default VCC/2

int getSmoothedValue(uint8_t pin_acs712);
int getCurrent(uint32_t adc) ;

#endif // _M_ACS712_H__