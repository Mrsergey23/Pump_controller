
#include "m_ACS712.h"

// average value of current value from "repeats" times
int getSmoothedValue(uint8_t value_ACS){
  int value;
  int repeats = 10;
  for (int i = 0; i < repeats; i++){ // measure current "repeats" times
    value += value_ACS; // суммируем измеренные значения
    delay(1);
  }
  value /= repeats; // и берём среднее арифметическое
  return value;
}