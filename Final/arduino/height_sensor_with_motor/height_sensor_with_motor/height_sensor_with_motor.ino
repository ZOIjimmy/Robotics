int motor1pin1 = 3;
int motor1pin2 = 2;

int Trig = 12;
int Echo = 13;

const int BUTTON_PIN = 7;  // 按鍵的接腳
int buttonState = 0;   // 按鈕的狀態

int Duration;
float Distance;

String command;
float degree;


int motorSugarPin1 = 4;
int motorSugarPin2 = 5;

int IR_Objects = 9; //紅外線接
int IR = 0; //紅外線初始值
int mem = 0;

const float speed = 360.0/4800.0;

void counterClockwise() {
    digitalWrite(motor1pin1, HIGH);
    digitalWrite(motor1pin2, LOW);
}

void StopCounterClockwise() {
    digitalWrite(motor1pin1, LOW);
}

void clockwise() {
    digitalWrite(motor1pin1, LOW);
    digitalWrite(motor1pin2, HIGH);
}

void StopClockwise() {
    digitalWrite(motor1pin2, LOW);
}

void turn(float degree) {
  if (degree > 0){
    clockwise();
    float total_delay = degree/speed;
    delay(total_delay);
    StopClockwise();
  }
}

void resetAngle() {
  counterClockwise();
  while( true )
  {
    buttonState = digitalRead(BUTTON_PIN);
    if(buttonState == LOW){
      Serial.println("button pressed");
      break;
    }
    delay(5);
  }
  StopCounterClockwise();
}

void getDis() {
  // ultra sonic sensor
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
  }
}


void sugar() {
  digitalWrite(motorSugarPin1, LOW);
  digitalWrite(motorSugarPin2, HIGH);
  delay(500);
  digitalWrite(motorSugarPin2, LOW);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);


  Serial.begin(9600);
  pinMode(Trig,OUTPUT);
  pinMode(Echo,INPUT);

  pinMode(BUTTON_PIN, INPUT);
}

void loop() {

    if(Serial.available()){
        command = Serial.readStringUntil('\n');
        // if(command.startsWith("turn")){
        //   if(Serial.available()){
        //     command = Serial.readStringUntil('\n');
          
        //     degree = command.toFloat();
        //     Serial.println(degree);              
        //     turn(degree);
        //   }
        // }
        if(command.equals("send")){
          getDis();
        }
        else if(command.equals("reset")) {
          resetAngle();
        }
        else if(command.equals("sugar")) {
          sugar();
        }
        else{
          degree = command.toFloat();
          Serial.println(degree);              
          turn(degree);
        }
    }

  delay(500);
}