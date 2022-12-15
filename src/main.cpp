/* ------------Description of the project---------------

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

//!! перестают высылаться данные посел перехода во второй режим работы

#include <Arduino.h>
#include <GyverTimers.h> // for interrupts by Timers and generating signals 
#include "m_ACS712.h"
// #include "m_FlowSensor_YF_S402B.h"
#include "m_ReceiveSendData.h"

/*--------------Defines of required pins---------------*/
#define ACS712_PIN  A0   // any analog pin. Current sensor ACS-712 30 A max. 
#define FLOW_PIN    2    // any input digital pin. Sensor YF-S402B. sensoring of flow liquid, like in our homes 
#define IN1         9   // 1 output of Timer 1, because it's 16  bits Timer. Motor driver 1 pin to choose diagonal of H-bridge (driver XY-160D)
#define IN2         10    // 2 output of Timer 1, second pin of motor driver to choose the other ddiagonal of H-bridge (driver XY-160D)
#define ENA         8    // any digital output pin, here we use it only for enable to rotate engine (HIGH signal) or disable (LOW signal) (driver XY-160D)
/*--------------End of defines--------------- */

/*define periods of timers on millis()*/
#define PERIOD_DATA_FROM_SENSORS 1000

/*--------------Information about driver and pump engine--------------*/
/*I am using driver in unnormal way. Ther normal way: Constant signal (
  HIGH or LOW to IN1 and LOW and HIGH (signals depends on direction, watch documentation) to IN2 and PWM to ENA, but i don't need to
  chose direction due to special design of motor of pump. In addition
  it is two-phase sensorless (without default Hall sensor) BLDC motor and I need
  special way to start-up and control this. Generating of two square signals by Tymer 1
  for IN1 and IN2 pins of motor driver I allow to generating bipolar square signal for this engine
*/
volatile uint16_t  P_pulse_Count;
uint32_t Current_Time, Loop_Time, Timer_stepper;
int16_t A_zero_level;
uint16_t A_current_calc, A_sensorValue, P_liter_per_hour; 
uint16_t data[10];
int send_pack[2]; // возможно изменить на int, как в оригинале
volatile int16_t start_freq,freq_step,
finish_freq, time_step;                       // variable for increasing speed at the start engine
void m_NeedStopAll();
void m_InitTimers();
void IRQ_flow();

void setup() 
{
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(FLOW_PIN, INPUT);  
  Serial.begin(115200);
  A_zero_level = getSmoothedValue(ACS712_PIN); // define zero scale (before turn on load)
  attachInterrupt(0, IRQ_flow, RISING);                              
  Current_Time = millis();
  Loop_Time = Current_Time;
  digitalWrite(FLOW_PIN, HIGH);     // optional internal pull-Up
  m_InitTimers();
}

void loop() 
{
  if (Serial.availableForWrite() > 0)         // waiting command by serial
  {
     
    Current_Time = millis();
    if(Current_Time >= (Loop_Time + PERIOD_DATA_FROM_SENSORS))
    {
      Loop_Time = Current_Time;
      P_liter_per_hour = (P_pulse_Count * 60 / 7.5);
      P_pulse_Count = 0;
      send_pack[0] = P_liter_per_hour;
      A_sensorValue = getSmoothedValue(ACS712_PIN); // читаем значение с АЦП и выводим в монитор
      A_current_calc = getCurrent(A_sensorValue); // преобразуем в значение тока и выводим в монитор
      send_pack[1] = A_current_calc; 
      m_SendData(0,send_pack, 3);
      // Serial.print(0);
      // Serial.print(',');
      // Serial.print(P_liter_per_hour);
      // Serial.print(',');
      // Serial.println(A_current_calc); 
    }
    m_ReceiveData(); // parsing of receiving command from GUI by UART
    switch (data[0])
    {

    case 0:
      Timer1.setFrequency(data[1]*2);
      digitalWrite(ENA, data[2]);
      break;

    case 1:
      start_freq = data[1];
      finish_freq = data[2];
      time_step = data[3];
      freq_step = data[5]; 
      // Timer0.setFrequency(2*1000/time_step); // проба сделать на встроенном таймере (пока не стал разбираться в ошибках)
      // Timer0.enableISR(CHANNEL_B);
      if (millis() - Timer_stepper >= time_step) 
      {   //Timer with period "time_step"
        Timer_stepper = millis();              // reset timer
        if (start_freq<=finish_freq)
        {
          start_freq += freq_step; 
        } 
      }
      while(start_freq < finish_freq)
      {
        Timer1.setFrequency(start_freq * 2);
      }
      break;
    default:
      m_NeedStopAll(); // проверка нужна ли остановка двигателей
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
void m_NeedStopAll()
{
    if ((data[1] & data[2] & data[3] & data[4]) == 0) // disconnect
  {
    digitalWrite(ENA, 0);
    //Timer0.disableISR(CHANNEL_B);
  }
}

void m_InitTimers()
{
  TCCR1A = (TCCR1A & 0xF0);
  TCCR1B = (1 << WGM13) | (1 << WGM12) ;
  Timer1.outputEnable(CHANNEL_A, TOGGLE_PIN);
  Timer1.outputEnable(CHANNEL_B, TOGGLE_PIN);
  Timer1.outputState(CHANNEL_A, HIGH);
  Timer1.outputState(CHANNEL_B, LOW); 
}

void IRQ_flow() // IRQ Handler (require interrupt 1 per 1 second)
{
    P_pulse_Count++;
}