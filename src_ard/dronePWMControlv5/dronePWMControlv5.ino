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

int pos = 0;    // variable to store the servo position

uint16_t pwm0 = 78;
uint16_t pwm1 = 78;
uint16_t pwm2 = 78;
uint16_t pwm3 = 78;
uint16_t pwm4 = 78;
uint16_t pwm5 = 78;

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
  myservo0.write(93);
  myservo1.write(93);
  myservo2.write(93);
  myservo3.write(93);
  myservo4.write(93);
  myservo5.write(93);

  Serial.println("ARD - OK\n");
  Serial.flush();
}

void loop() {
  myservo0.write(pwm0);
  myservo1.write(pwm1);
  myservo2.write(pwm2);
  myservo3.write(pwm3);
  myservo4.write(pwm4);
  myservo5.write(pwm5);

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

    pwm0 = inputString.substring(inputString.indexOf('a')+1, inputString.indexOf('b')).toInt();
    pwm1 = inputString.substring(inputString.indexOf('b')+1, inputString.indexOf('c')).toInt();
    pwm2 = inputString.substring(inputString.indexOf('c')+1, inputString.indexOf('d')).toInt();
    pwm3 = inputString.substring(inputString.indexOf('d')+1, inputString.indexOf('e')).toInt();
    pwm4 = inputString.substring(inputString.indexOf('e')+1, inputString.indexOf('f')).toInt();
    pwm5 = inputString.substring(inputString.indexOf('f')+1, inputString.indexOf('g')).toInt();
}
