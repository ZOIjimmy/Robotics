int Trig = 12;

int Echo = 13;

int Duration;

float Distance;

void setup() {

  Serial.begin(9600);

  pinMode(Trig,OUTPUT);

  pinMode(Echo,INPUT);

}

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
    
  }

  delay(500);

}

