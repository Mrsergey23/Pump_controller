#include "m_system_init.h"
#include <GyverTimers.h> // for interrupts by Timers and generating signals 
#include "config.h"

void m_TimerInit()
{
  TCCR1A = (TCCR1A & 0xF0);
  TCCR1B = (1 << WGM13) | (1 << WGM12) ;
  Timer1.outputEnable(CHANNEL_A, TOGGLE_PIN);
  Timer1.outputEnable(CHANNEL_B, TOGGLE_PIN);
  Timer1.outputState(CHANNEL_A, HIGH);
  Timer1.outputState(CHANNEL_B, LOW); 
  TCCR1A = TCCR1A & 0x0F;
}

void m_PinsInit()
{
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT); 
}