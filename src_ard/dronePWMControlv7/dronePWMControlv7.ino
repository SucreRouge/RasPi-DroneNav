#include <Servo.h>

#define PREAMBLE       0xAA
#define MSG_SIZE       7

uint8_t dataBuffer[MSG_SIZE - 1];

Servo myservo0;  // create servo object to control a servo
Servo myservo1;  // create servo object to control a servo
Servo myservo2;  // create servo object to control a servo
Servo myservo3;  // create servo object to control a servo
Servo myservo4;  // create servo object to control a servo
Servo myservo5;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int16_t pwm0 = 1500;
int16_t pwm1 = 1500;
int16_t pwm2 = 1500;
int16_t pwm3 = 1500;
int16_t pwm4 = 1500;
int16_t pwm5 = 1500;

void setup() {
    Serial.begin(115200);
    myservo0.attach(14);
    myservo1.attach(15);
    myservo2.attach(16);
    myservo3.attach(17);
    myservo4.attach(18);
    myservo5.attach(19);

    // set initial PWM signals
    myservo0.writeMicroseconds(1500);
    myservo1.writeMicroseconds(1500);
    myservo2.writeMicroseconds(1500);
    myservo3.writeMicroseconds(1500);
    myservo4.writeMicroseconds(1500);
    myservo5.writeMicroseconds(1500);

    Serial.println("ARD - OK\n");
    Serial.flush();
}

void loop() {
    // set PWM signals
    myservo0.writeMicroseconds(pwm0);
    myservo1.writeMicroseconds(pwm1);
    myservo2.writeMicroseconds(pwm2);
    myservo3.writeMicroseconds(pwm3);
    myservo4.writeMicroseconds(pwm4);
    myservo5.writeMicroseconds(pwm5);
}

void serialEvent() {
    // Serial.available returns number of elements in Serial buffer
    if (Serial.available() >= MSG_SIZE) {
        // get the first byte from buffer
        uint8_t inChar = (uint8_t)Serial.read();

        if(inChar == PREAMBLE){
            Serial.readBytes(dataBuffer, MSG_SIZE - 1);

            pwm0 = dataBuffer[0] * 10;
            pwm1 = dataBuffer[1] * 10;
            pwm2 = dataBuffer[2] * 10;
            pwm3 = dataBuffer[3] * 10;
            pwm4 = dataBuffer[4] * 10;
            pwm5 = dataBuffer[5] * 10;
        }
    }
}
