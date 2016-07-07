String inputString = "";
boolean stringComplete = false;

void setup() {
    Serial.begin(115200);

    while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
    }

    // reserve 200 bytes for the inputString
    inputString.reserve(200);
    // PWM pins to output
    DDRB |= 0b00001110;
    DDRD |= 0b01101000;

    // synchronization info for RPi
    Serial.println("ARD - OK\n");
}


void loop() {
    if (stringComplete) {
        Serial.println(inputString);

        // HERE IT WOULD GENERATED PWM SIGNALS


        // clear the string
        inputString = "";
        stringComplete = false;
    }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
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
}
