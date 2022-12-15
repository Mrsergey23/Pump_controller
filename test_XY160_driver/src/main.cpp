#include <Arduino.h>
#include <GyverTimers.h>


// Протестить смену таймера по прерыванию от другого таймера на тестовой программе (test) в стандартной VScode папке, либо просто измененение 
// переменной внутри прерывания и увеличения на нее за пределами
#include  <PWM.h>

const int IN1 = 11; //forward
const int IN2 = 3; //back
const int ENA = 9;

int data[10];

void initTimers()
{
    // из-за особенности генерации меандра таймером
  // частоту нужно указывать в два раза больше нужной!
  Timer2.outputEnable(CHANNEL_A, TOGGLE_PIN);   // в момент срабатывания таймера пин будет переключаться
  Timer2.outputEnable(CHANNEL_B, TOGGLE_PIN);   // в момент срабатывания таймера пин будет переключаться

  Timer2.outputState(CHANNEL_A, HIGH);          // задаём начальное состояние пина 11
  Timer2.outputState(CHANNEL_B, LOW);           // задаём начальное состояние пина 3
  //TCCR2B = (TCCR2B & 0x7F) | (0x00 << FOC2A)|(TCCR2B & 0xBF) | (0x01 << FOC2B);  //case CHANNEL_A: #define CHANNEL_A 0x00 //case CHANNEL_B: #define CHANNEL_B 0x01
 
}

void setup(){
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT); // для отладки millis
  Serial.begin(9600);
  //InitTimersSafe(); 
}
volatile int start_freq;
volatile int finish_freq;
volatile int freq_step;
void loop()
{
  if (Serial.available()>1)
  {
    char str[30];
    int amount = Serial.readBytesUntil(';', str, 30);
    str[amount] = NULL;

    
    int count = 0;
    char* offset = str;
    while (true){
      data[count++] = atoi(offset);
      offset = strchr(offset, ',');
      if (offset) offset++;
      else break;
    }
  // brightness ++;
    switch (data[0])
    {
    case 0:
      initTimers();
      Timer2.setFrequency(data[1] * 2);               // настроить частоту в Гц и запустить таймер.
      digitalWrite(ENA, data[2]);
      if (data[1]==0)
      { 
        Timer2.outputDisable(CHANNEL_B);
        Timer2.outputDisable(CHANNEL_A);
      }
      break;

    case 1:
      initTimers();
      start_freq = data[1];
      finish_freq = data[2];
      freq_step = data[5];
   

      if (data[1]|data[2]|data[3]|data[5]==0)
      {
        Timer1.disableISR(CHANNEL_B);
        Timer2.outputDisable(CHANNEL_B);
        Timer2.outputDisable(CHANNEL_A);
      }
      int time_step = data[3];              
      Timer1.setFrequency(2*1000/time_step);
      Timer1.enableISR(CHANNEL_B);                   // Запускаем прерывание (по умолч. канал А)
      initTimers();
      while(start_freq<finish_freq)
      {
        Timer2.setFrequency(start_freq * 2);
      }
    break;   

    case 2:
     // режим заполнения Шима высокачасатотным ШИМом
    break; 
    
    }
  }
}


ISR(TIMER1_B)
{ 
  if (start_freq<=finish_freq)
  {
    start_freq += freq_step; 
  }
     
}


// стандартные типы команд, для однополярного ШИМа
void Motor1_Forward(int Speed)
{
 digitalWrite(IN1,HIGH);
 digitalWrite(IN2,LOW); 
 SetPinFrequency(ENA, 50);
 pwmWrite(ENA, 50);
 //analogWrite(ENA,Speed);
}
 
void Motor1_Backward(int Speed)
{ 
 digitalWrite(IN1,LOW);
 digitalWrite(IN2,HIGH); 
 analogWrite(ENA,Speed);
}

void Motor1_Brake() 
{
 digitalWrite(IN1,LOW);
 digitalWrite(IN2,LOW);
} 