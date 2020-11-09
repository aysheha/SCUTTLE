/* This program uses an arduino to convert ADC signals from an 
 * HX711 loadcell interface's propreitary protocol to i2c 
 * so a Beaglebone can read it
 * It uses example code from both the HX711 library and the adafruit wire library
 */

#include "HX711.h"
#include <Wire.h>

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;
long reading;

HX711 scale;

void setup() {
  Serial.begin(115200);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  Wire.begin(8);                // join i2c bus with address #8
  
}

void loop() {

  if (scale.is_ready()) {
    reading = scale.read();
    Serial.print("HX711 reading: ");
    Serial.println(reading);
  } else {
    Serial.println("HX711 not found.");
  }

  Wire.onRequest(reading); // register event
  delay (100);
}
