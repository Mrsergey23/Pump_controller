#ifndef _M_FLOW_SENSOR_YF_S402B__
#define _M_FLOW_SENSOR_YF_S402B__
#include <Arduino.h>
extern uint32_t Current_Time, Loop_Time;
extern uint16_t P_liter_per_hour;
void IRQ_flow(); // IRQ Handler (requre interrupt 1 per 1 second)
void m_GetValue_FlowSensor();


#endif //_M_FLOW_SENSOR_YF_S402B__