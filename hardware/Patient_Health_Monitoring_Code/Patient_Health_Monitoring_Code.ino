#include <TimerOne.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(17, 16, 6, 7, 8, 9);

int val;
int tempPin = 36;
int HBSensor = 14;
int HBCount = 0;
int HBCheck = 0;
int TimeinSec = 0;
int HBperMin = 0;
int HBStart = 31;
int HBStartCheck = 0;
int buzzerPin = 11;

void setup() {
  Serial.begin(9600);
  lcd.begin(20, 4);
  pinMode(HBSensor, INPUT);
  pinMode(HBStart, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);
  Timer1.initialize(800000); 
  Timer1.attachInterrupt( timerIsr );
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("HEALTH MONITORING");
  lcd.setCursor(0,1);
  lcd.print("TIME IN SEC : ");
  lcd.setCursor(0,2);
  lcd.print("HB PER MIN  : ");
}

void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read();
    if (received == '1') {
      HBStartCheck = 1;
    }
  }

  if(HBStartCheck == 1) {
    if((digitalRead(HBSensor) == HIGH) && (HBCheck == 0)) {
      HBCount = HBCount + 1;
      HBCheck = 1;
    }
    
    if((digitalRead(HBSensor) == LOW) && (HBCheck == 1)) {
      HBCheck = 0;   
    }
    
    if(TimeinSec == 10) {
      HBperMin = HBCount * 6;;
      HBStartCheck = 0;
      lcd.setCursor(14,2);
      lcd.print(HBperMin);
      lcd.print(" ");
      Serial.print(" Heart Rate: ");
      Serial.println(HBperMin);
      HBCount = 0;
      TimeinSec = 0;
      digitalWrite(buzzerPin, HIGH);
      delay(1000);
      digitalWrite(buzzerPin, LOW);
    }
  }
}

void timerIsr() {
  if(HBStartCheck == 1) {
    TimeinSec = TimeinSec + 1;
    lcd.setCursor(14,1);
    lcd.print(TimeinSec);
    lcd.print(" ");
  }
}
