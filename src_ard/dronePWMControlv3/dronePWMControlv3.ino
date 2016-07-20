String inputString = "";
boolean stringComplete = false;
boolean synchronized = false;
uint16_t m = 0;
uint16_t period = 1050;

bool On0 = false;
bool On1 = false;
bool On2 = false;
bool On3 = false;
bool On4 = false;
bool On5 = false;
// bool On6 = false;
// bool On7 = false;


uint16_t pwm0 = 78;
uint16_t pwm1 = 78;
uint16_t pwm2 = 78;
uint16_t pwm3 = 78;
uint16_t pwm4 = 78;
uint16_t pwm5 = 78;
// uint16_t pwm6 = 103;
// uint16_t pwm7 = 103;


// 1  ms
//a052b052c052d052e052f052g
// 1.5ms
//a078b078c078d078e078f078g
// 2  ms
//a103b103c103d103e103f103g
//a999b999c999d999e999f999g
void setup() {
    Serial.begin(115200);

    // reserve 200 bytes for the inputString
    inputString.reserve(64);
    // PWM pins to output
    DDRC |= 0b00111111;
    // DDRD |= 0b01100000;

    //while (!Serial) {
    // wait for serial port to connect. Needed for native USB port only
    PORTC |= _BV(PC5);
    delay(2000);
    PORTC &= ~_BV(PC5);
    delay(2000);
    //}

    // synchronization info for RPi
    Serial.println("ARD - OK\n");
    Serial.flush();
}


void loop() {
    char inChar = (char)Serial.read();
    // add it to the inputString:
    //if(!synchronized && inChar == 'a'){
    //    synchronized = true;
    //}
    if (isdigit(inChar) || isalpha(inChar)){
        inputString += inChar;
    }
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
        stringComplete = true;
    }

    if(stringComplete){
        pwm0 = inputString.substring(inputString.indexOf('a')+1, inputString.indexOf('b')).toInt();
        pwm1 = inputString.substring(inputString.indexOf('b')+1, inputString.indexOf('c')).toInt();
        pwm2 = inputString.substring(inputString.indexOf('c')+1, inputString.indexOf('d')).toInt();
        pwm3 = inputString.substring(inputString.indexOf('d')+1, inputString.indexOf('e')).toInt();
        pwm4 = inputString.substring(inputString.indexOf('e')+1, inputString.indexOf('f')).toInt();
        pwm5 = inputString.substring(inputString.indexOf('f')+1, inputString.indexOf('g')).toInt();
        inputString = "";
        stringComplete = false;
    }

//    // low state
//    PORTC &= 0b11000000;
//    PORTD &= 0b10011111;
//
//    // high state
//    PORTC |= 0b00111111;
//    PORTD |= 0b01100000;

// high
//PORTC |= _BV(PD7);
// low
//PORTC &= ~_BV(PD7);

////////////////////                                     0
    if (m <= pwm0 && On0 == false){
        PORTC |= _BV(PC0);
        On0 = true;
    }
    if (m > pwm0 && On0 == true){
        PORTC &= ~_BV(PC0);
        On0 = false;
    }
////////////////////                                     1
    if (m <= pwm1 && On1 == false){
        PORTC |= _BV(PC1);
        On1 = true;
    }
    if (m > pwm1 && On1 == true){
        PORTC &= ~_BV(PC1);
        On1 = false;
    }
////////////////////                                     2
    if (m <= pwm2 && On2 == false){
        PORTC |= _BV(PC2);
        On2 = true;
    }
    if (m > pwm2 && On2 == true){
        PORTC &= ~_BV(PC2);
        On2 = false;
    }
////////////////////                                     3
    if (m <= pwm3 && On3 == false){
        PORTC |= _BV(PC3);
        On3 = true;
    }
    if (m > pwm3 && On3 == true){
        PORTC &= ~_BV(PC3);
        On3 = false;
    }
////////////////////                                     4
    if (m <= pwm4 && On4 == false){
        PORTC |= _BV(PC4);
        On4 = true;
    }
    if (m > pwm4 && On4 == true){
        PORTC &= ~_BV(PC4);
        On4 = false;
    }
////////////////////                                     5
    if (m <= pwm5 && On5 == false){
        PORTC |= _BV(PC5);
        On5 = true;
    }
    if (m > pwm5 && On5 == true){
        PORTC &= ~_BV(PC5);
        On5 = false;
    }
 // ////////////////////                                     6
 //    if (m <= pwm6 && On6 == false){
 //        PORTD |= _BV(PD5);
 //        On6 = true;
 //    }
 //    if (m > pwm6 && On6 == true){
 //        PORTD &= ~_BV(PD5);
 //        On6 = false;
 //    }
 // ////////////////////                                     7
 //    if (m <= pwm7 && On7 == false){
 //        PORTD |= _BV(PD6);
 //        On7 = true;
 //    }
 //    if (m > pwm7 && On7 == true){
 //        PORTD &= ~_BV(PD6);
 //        On7 = false;
 //    }


    m = m + 1;

    if (m >= period){
        m = 0;
    }

}
