char inputString[] = "a078b078c078d078e078f078g\n";
char numberBuffer[4] = {'0','0','0','\0'};
char syncSymbol[1] = {'a'};
boolean stringComplete = false;
boolean synchronized = false;
uint16_t m = 0;
uint16_t period = 1050;
char* p1 = NULL;
char* p2 = NULL;

bool On0 = false;
bool On1 = false;
bool On2 = false;
bool On3 = false;
bool On4 = false;
bool On5 = false;

uint16_t pwm0 = 78;
uint16_t pwm1 = 78;
uint16_t pwm2 = 78;
uint16_t pwm3 = 78;
uint16_t pwm4 = 78;
uint16_t pwm5 = 78;

// 1  ms
//a052b052c052d052e052f052g
// 1.5ms
//a078b078c078d078e078f078g
// 2  ms
//a103b103c103d103e103f103g
//a999b999c999d999e999f999g
void setup() {
    Serial.begin(115200);
    // PWM pins to output
    DDRC |= 0b00111111;

    PORTC |= _BV(PC5);
    delay(2000);
    PORTC &= ~_BV(PC5);
    delay(2000);

    Serial.println("ARD - OK\n");
    Serial.flush();

    // clear inputString to append to it later
    strcpy(inputString, "");
}


void loop() {
    char inChar = (char)Serial.read();
    // add it to the inputString:
    if(!synchronized && strcmp(&inChar, syncSymbol)){
        synchronized = true;
    }

    if (isdigit(inChar) || isalpha(inChar) && synchronized){
        strcat(inputString, &inChar);
    }
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
        stringComplete = true;
    }

    if(stringComplete){
        // hold the adress of the first 'a' occurence
        p1 = strchr(inputString, 'a');
        p2 = strchr(inputString, 'b');
        // substracting the ADRESSES!!!
        memcpy(numberBuffer, p1+1, p2 - p1);
        numberBuffer[3] = '\0';
        pwm0 = atoi(numberBuffer);

        p1 = strchr(inputString, 'b');
        p2 = strchr(inputString, 'c');
        // substracting the ADRESSES!!!
        memcpy(numberBuffer, p1+1, p2 - p1);
        numberBuffer[3] = '\0';
        pwm1 = atoi(numberBuffer);

        p1 = strchr(inputString, 'c');
        p2 = strchr(inputString, 'd');
        // substracting the ADRESSES!!!
        memcpy(numberBuffer, p1+1, p2 - p1);
        numberBuffer[3] = '\0';
        pwm2 = atoi(numberBuffer);

        p1 = strchr(inputString, 'd');
        p2 = strchr(inputString, 'e');
        // substracting the ADRESSES!!!
        memcpy(numberBuffer, p1+1, p2 - p1);
        numberBuffer[3] = '\0';
        pwm3 = atoi(numberBuffer);

        p1 = strchr(inputString, 'e');
        p2 = strchr(inputString, 'f');
        // substracting the ADRESSES!!!
        memcpy(numberBuffer, p1+1, p2 - p1);
        numberBuffer[3] = '\0';
        pwm4 = atoi(numberBuffer);

        p1 = strchr(inputString, 'f');
        p2 = strchr(inputString, 'g');
        // substracting the ADRESSES!!!
        memcpy(numberBuffer, p1+1, p2 - p1);
        numberBuffer[3] = '\0';
        pwm5 = atoi(numberBuffer);

        Serial.print(inputString);
        strcpy(inputString, "");
        stringComplete = false;
    }

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

    m = m + 1;

    if (m >= period){
        m = 0;
    }
}
