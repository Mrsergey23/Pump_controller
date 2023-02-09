#ifndef _M_FLOW_SENSOR_YF_S402B__
#define _M_FLOW_SENSOR_YF_S402B__


void m_Flow_init(const uint8_t flow_pin);
uint16_t m_GetValue_FlowSensor(const uint16_t period_sec);
void IRQ_flow(); // IRQ Handler (requre interrupt 1 per 1 second)



#endif //_M_FLOW_SENSOR_YF_S402B__