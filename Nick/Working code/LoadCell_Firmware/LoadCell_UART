/*This code converts Hx711 data to UART on an arduino nano
 * This uses the Hx711 and adafruit serial libraries
 * use this to communicate with the beaglebone blue
 * nano ------------->beaglebone
 * TX1  -------------> UART RX#
 * RX0  -------------> UART TX#
 * Vin  -------------> 5v (usb can also be used for power)
 * GND  -------------> GND
 * 
 * HX711-------------> nano
 * DT   -------------> D2 (this the green jumper)
 * CLK  -------------> D3 (yellow Jumper)
 * VCC  -------------> 5V (orange)
 * GND  -------------> GND (purple)
 */

#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;

HX711 scale;

void setup() {
  Serial.begin(9600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}

void loop() {

  if (scale.is_ready()) {
    long reading = scale.read();
    Serial.print(reading);
    
  } else {
    Serial.println("ns");
  }

  delay(100);
  
}
