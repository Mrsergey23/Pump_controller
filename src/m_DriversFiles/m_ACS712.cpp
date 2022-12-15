
#include "m_ACS712.h"

// рассчитывает ток в мА по значению с АЦП
int getCurrent(uint32_t adc) {
  int delta = A_zero_level - adc; // отклонение от нуля шкалы
  float scale = 37.888; // сколько единиц АЦП приходится на 1 ампер
  int current = (int)delta*1000/scale; // считаем ток в мА
  return current;
}

// average value of current value from "repeats" times
int getSmoothedValue(uint8_t pin_acs712){
  int value;
  int repeats = 10;
  for (int i = 0; i < repeats; i++){ // measure current "repeats" times
    value += analogRead(pin_acs712); // суммируем измеренные значения
    delay(1);
  }
  value /= repeats; // и берём среднее арифметическое
  return value;
}