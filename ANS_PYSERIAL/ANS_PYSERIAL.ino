/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int mid_angle = 70;
int left_angle = 60;
int right_angle = 80;
int straight_speed = 70;
int turn_speed = 70;
int _speed = 0;
void setup() {
  myservo.attach(9); // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  myservo.write(mid_angle);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
}

void loop() {
 
  if (Serial.available() > 0 ) {
     int angle = Serial.parseInt();
     if ( angle == 999 ) {
        _speed = 0;
     }
     else if ( angle == mid_angle ) {
         _speed = straight_speed;
         myservo.write(mid_angle);
     }
     else if ( angle == left_angle ) {
        _speed = turn_speed;
        myservo.write(left_angle);
     }
     else if ( angle == right_angle ) {
      _speed = turn_speed;
      myservo.write(right_angle);
     }
     else {
      myservo.write(mid_angle);
      _speed = 0;
     }
     
     analogWrite(6, _speed);
     analogWrite(5,0);
  }
  else {
     analogWrite(6, 0);
     analogWrite(5,0);
  }
  delay(250);
}
