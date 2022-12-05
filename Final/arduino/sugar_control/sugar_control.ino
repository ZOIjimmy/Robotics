#include <Servo.h>   //載入函式庫，這是內建的，不用安裝

Servo myservo;

int IR_Objects = 3; //紅外線接
int IR = 0; //紅外線初始值

void setup() {
  Serial.begin(9600);
  pinMode(IR_Objects,INPUT); //定義紅外線為輸入端
  myservo.attach(9);
}

void loop() {
  IR=digitalRead(IR_Objects); //　定義IR_Objects=IR 並為讀取紅外線狀態
  if(IR == LOW) //假設紅外線等於高電平
  {
    delay(1500);
    myservo.attach(9);
    myservo.write(160);
    delay(1000);
    myservo.detach();
    delay(1000);
    Serial.println("yes");
    delay(IR); // 　延遲時間等於IR作動時間
  }
  else
  {
    myservo.detach();
     Serial.println("no");
  }
}