#include <Servo.h>

String inputString = "";
boolean stringComplete = false;
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

  //142 = 2.008ms
  //45 = 1.008ms
  //93 = 1.502ms
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
  myservo0.writeMicroseconds(pwm0);
  myservo1.writeMicroseconds(pwm1);
  myservo2.writeMicroseconds(pwm2);
  myservo3.writeMicroseconds(pwm3);
  myservo4.writeMicroseconds(pwm4);
  myservo5.writeMicroseconds(pwm5);

    if(stringComplete){
        inputString = "";
        stringComplete = false;
    }
}

void serialEvent() {
    while (Serial.available()) {
         // get the new byte:
        char inChar = (char)Serial.read();
        // add it to the inputString:
        inputString += inChar;
        // if the incoming character is a newline, set a flag
        // so the main loop can do something about it:
        if (inChar == '\n') {
            stringComplete = true;
        }
    }

    if (stringComplete)
    {
      pwm0 = inputString.substring(inputString.indexOf('a')+1, inputString.indexOf('b')).toInt();
      pwm1 = inputString.substring(inputString.indexOf('b')+1, inputString.indexOf('c')).toInt();
      pwm2 = inputString.substring(inputString.indexOf('c')+1, inputString.indexOf('d')).toInt();
      pwm3 = inputString.substring(inputString.indexOf('d')+1, inputString.indexOf('e')).toInt();
      pwm4 = inputString.substring(inputString.indexOf('e')+1, inputString.indexOf('f')).toInt();
      pwm5 = inputString.substring(inputString.indexOf('f')+1, inputString.indexOf('g')).toInt();

      pwm0 = pwm0 * 10;
      pwm1 = pwm1 * 10;
      pwm2 = pwm2 * 10;
      pwm3 = pwm3 * 10;
      pwm4 = pwm4 * 10;
      pwm5 = pwm5 * 10;

    }
}
