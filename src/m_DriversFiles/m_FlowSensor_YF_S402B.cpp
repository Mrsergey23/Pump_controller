#include <Arduino.h>
#include "m_FlowSensor_YF_S402B.h"

volatile uint16_t  P_pulse_Count;
uint16_t  P_liter_per_period;

void m_Flow_init(uint8_t flow_pin)
{
  pinMode(flow_pin, INPUT); 
  attachInterrupt(0, IRQ_flow, RISING);                              
  digitalWrite(flow_pin, HIGH);     // optional internal pull-Up
}

uint16_t m_GetValue_FlowSensor(uint16_t period_sec)
{
    P_liter_per_period = (P_pulse_Count * period_sec / 7.5);
    P_pulse_Count = 0;
    return P_liter_per_period;
}

void IRQ_flow() // IRQ Handler (requre interrupt 1 per 1 second)
{
    P_pulse_Count++;
}
