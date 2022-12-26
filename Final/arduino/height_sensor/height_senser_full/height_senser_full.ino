#include "Arduino.h"
#include <SoftwareSerial.h>

const byte rxPin = 9;
const byte txPin = 8;
SoftwareSerial BTSerial(rxPin, txPin); // RX TX

int Trig = 12;

int Echo = 13;

int Duration;

float Distance;

void setup() {
  pinMode(Trig,OUTPUT);
  pinMode(Echo,INPUT);

  // define pin modes for tx, rx:
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  
  BTSerial.begin(9600);
  Serial.begin(9600);
}

String messageBuffer = "";
String message = "";

void loop() {

  digitalWrite(Trig,LOW);

  delayMicroseconds(1);

  digitalWrite(Trig,HIGH);

  delayMicroseconds(11);

  digitalWrite(Trig,LOW);

  Duration = pulseIn(Echo,HIGH);

  if (Duration>0) {

    Distance = Duration/2;

    Distance = Distance*340*100/1000000; // ultrasonic speed is 340m/s = 34000cm/s = 0.034cm/us

    Serial.print(Distance);

    Serial.println("cm");

    Serial.print(Duration);

    Serial.print("us");

    BTSerial.print(Distance);
    BTSerial.print(Duration);
  }

  delay(500);

}

