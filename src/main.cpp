/* ------------Description of the project--------------------------*/
/*
Latest version of project pump, which called Acquastream XT
  Trying to start up the engine, because the electric part of device
was burned or broken. 
  The main case is to create circuit for control systems and
make it unmanned with adaptive algorithm.
  The target of this pump is array of diods for activation of
main elemant of LAZER system.  

  There are 2 main versions of control engine:
  1) constant frequency (operating mode = around 49-55 Hz)
  2) start-up with smooth inscreasing of frequency (need to define 
  4 parameters: start_freq, finish_freq, time_step, freq_step. It means interupt with period time_step
  to increment up with freq_step.
*/
#include <Arduino.h>
#include <GyverTimers.h> // for interrupts by Timers and generating signals 
#include "m_FlowSensor_YF_S402B.h"
#include "ACS712.h"
#include "m_ReceiveSendData.h"
#include "config.h"
#include "m_system_init.h"
/*--------------Information about driver and pump engine-----------*/
/*
  I am using driver in unnormal way. Ther normal way: Constant signal (
  HIGH or LOW to IN1 and LOW and HIGH (signals depends on direction, watch documentation) to IN2 and PWM to ENA, but i don't need to
  chose direction due to special design of motor of pump. In addition
  it is two-phase sensorless (without default Hall sensor) BLDC motor and I need
  special way to start-up and control this. Generating of two square signals by Tymer 1
  for IN1 and IN2 pins of motor driver I allow to generating bipolar square signal for this engine
*/
/* global variables */
float I_ACS_value; 
extern uint16_t P_flow_sensor_value;

uint32_t Current_Time, Loop_Time, \
Timer_stepper, loop_accelerating;
int16_t A_zero_level;
uint16_t A_current_calc, A_sensorValue; // variables hold the 
uint16_t data[10];                      // array of receiving data
bool flag;
int send_pack[2];                       // array to collect for data transmission                      
uint16_t freq_step, finish_freq, \
time_step, total_freq, start_freq;      // variable for increasing speed at the start engine

ACS712 sensor(ACS712_30A, A0);          // make an example of class for ACS712 current sensor

void m_StopAll();

void setup() 
{
  m_TimerInit();
  m_PinsInit();
  Serial.begin(115200);
  sensor.calibrate();                    // calibrate zero level of ACS712
  m_Flow_init(FLOW_PIN);
}

void loop() 
{
  if (Serial.availableForWrite() > 0)         // waiting command by serial
  {
    Current_Time = millis();
    if(Current_Time >= (Loop_Time + PERIOD_DATA_FROM_SENSORS))
    {
      Loop_Time = Current_Time;
      send_pack[0] = m_GetValue_FlowSensor(PERIOD_DATA_FROM_SENSORS);
      I_ACS_value = sensor.getCurrentDC();           // receive ampers
      send_pack[1] = I_ACS_value*100;                //convert to mA     
      m_SendData(0,send_pack, 2);
    }  
    m_ReceiveData(); // parsing of receiving command from GUI by UART
    switch (data[0])
    {
    case CONST_FREQ: // Const frequency mode
      TCCR1A = (TCCR1A&0x0F)|1<<6|1<<4; 
      Timer1.setFrequency(data[1]*2);
      digitalWrite(ENA, data[2]);
      break;

    case STOP_ALL: 
      digitalWrite(ENA, 0);
      break;

    case ACCEL_ON: // Accelearating mode
      TCCR1A = (TCCR1A&0x0F)|1<<6|1<<4;
      start_freq = data[1];
      finish_freq = data[2];
      time_step = data[3];
      freq_step = data[5]; 
      digitalWrite(ENA, 1);
      while (start_freq <= finish_freq)
      {
      Timer_stepper = millis();
        if (Timer_stepper >= loop_accelerating + time_step) 
        {   //Timer with period "time_step"
          loop_accelerating = Timer_stepper;           // reset timer
          Timer1.setFrequency(start_freq * 2);
          send_pack[0] = m_GetValue_FlowSensor(PERIOD_DATA_FROM_SENSORS);
          I_ACS_value = sensor.getCurrentDC();
          send_pack[1] = I_ACS_value*100; 
          m_SendData(0,send_pack, 2);
          start_freq +=  freq_step; 
        }
      }

      break;

      // Timer0.setFrequency(2*1000/time_step); // проба сделать на встроенном таймере (пока не стал разбираться в ошибках)
      // Timer0.enableISR(CHANNEL_B);

    default:
      m_StopAll(); // проверка нужна ли остановка двигателей
      break;
    }
  }
}


// ISR(TIMER0_B)
// { 
//   if (start_freq<=finish_freq)
//   {
//     start_freq += freq_step; 
//   }  
// }

/* Check the stop signal from GUI*/
void m_StopAll()
{
    if ((data[1] & data[2] & data[3] & data[4]) == 0) // disconnect
  {
    digitalWrite(ENA, 0); 
    //Timer0.disableISR(CHANNEL_B);
  }
}
