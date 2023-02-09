#ifndef __CONFIG_H_
#define __CONFIG_H_

/*--------------Defines of required pins---------------------------*/
#define ACS712_PIN  A0    // any analog pin. Current sensor ACS-712 30 A max. 
#define FLOW_PIN    2     // any input digital pin. Sensor YF-S402B. sensoring of flow liquid, like in our home bathrooms 
#define IN1         9     // 1 output of Timer 1, because it's 16  bits Timer. Motor driver 1 pin to choose diagonal of H-bridge (driver XY-160D)
#define IN2         10    // 2 output of Timer 1, second pin of motor driver to choose the other ddiagonal of H-bridge (driver XY-160D)
#define ENA         8     // any digital output pin, here we use it only for enable to rotate engine (HIGH signal) or disable (LOW signal) (driver XY-160D)
/*--------------End of defines-------------------------------------*/

/* define periods of timers on millis() */
#define PERIOD_DATA_FROM_SENSORS 10

/* define comannds for controling by UART ("cases") */
#define CONST_FREQ  3
#define STOP_ALL    2
#define ACCEL_ON    4 

#endif //__CONFIG_H_