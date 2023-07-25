const int m1_a = 3; //right rear motor 1
const int m1_b = 2; //right rear motor 1
const int m2_a = 4; //left rear motor 2
const int m2_b = 5; //left rear motor 2

const int steer_m1 = 6; //steer motor(IN1)
const int steer_m2 = 7; //steer motor(IN2)

const int TRIG1 = 22;    //left ultrasonic trig
const int ECHO1 = 23;   //left ultrasonic echo
const int TRIG2 = 24;    //right ultrasonic trig
const int ECHO2 = 25;   //right ultrasonic echo
const int TRIG3 = 27;    //front ultrasonic trig
const int ECHO3 = 26;   //front ultrasonic echo

const int pot = A0;
const int minPot =665;  //나중에 수정 필요
const int maxPot = 465;

const int MAX_DISTANCE = 2000;  //for ideal can detect for about 4m

const int angle_defalut = 565;  //need to check the potentiometer

int mode = 0;   //0: driving, 1: avoidance, 2:parking

bool start = false; //start sign

void hold()
{
    //stop
    analogWrite(steer_m1, LOW);
    analogWrite(steer_m2, LOW);
    
    analogWrite(m1_a, LOW);
    analogWrite(m1_b, LOW);
    analogWrite(m2_a, LOW);
    analogWrite(m2_b, LOW);
}

void left(int steer = 60, int speed = 100)
{
    //left
    steering(-1*steer);

    analogWrite(m1_a, speed);
    analogWrite(m1_b, LOW);
    analogWrite(m2_a, speed);
    analogWrite(m2_b, LOW);
}

void right(int steer = 60, int speed = 100)
{
    //right
    steering(steer);
    
    analogWrite(m1_a, speed);
    analogWrite(m1_b, LOW);
    analogWrite(m2_a, speed);
    analogWrite(m2_b, LOW);
}

void straight(int speed = 100)
{
    //straight
    steering(0);

    analogWrite(m1_a, speed);
    analogWrite(m1_b, LOW);
    analogWrite(m2_a, speed);
    analogWrite(m2_b, LOW);
}

void backward(int speed = 60)
{
  // backward
  steering(0);

  analogWrite(m1_a, LOW);
  analogWrite(m1_b, speed);
  analogWrite(m2_a, LOW);
  analogWrite(m2_b, speed);
}

void backleft(int steer = 60, int speed = 60)
{
    //left
    steering(-1*steer);

    analogWrite(m1_b, speed);
    analogWrite(m1_a, LOW);
    analogWrite(m2_b, speed);
    analogWrite(m2_a, LOW);
}

void backright(int steer = 60, int speed = 60)
{
    //right
    steering(steer);
    
    analogWrite(m1_b, speed);
    analogWrite(m1_a, LOW);
    analogWrite(m2_b, speed);
    analogWrite(m2_a, LOW);
}

void tok_left(int steer = 60, int speed = 100)
{
    //left
    steering(-1*steer);

    analogWrite(m1_a, speed);
    analogWrite(m1_b, LOW);
    analogWrite(m2_a, (int)(speed*1.2));
    analogWrite(m2_b, LOW);
}

void tok_right(int steer = 60, int speed = 100)
{
    //right
    steering(steer);

    analogWrite(m1_a, (int)(speed*1.2));
    analogWrite(m1_b, LOW);
    analogWrite(m2_a, speed);
    analogWrite(m2_b, LOW);
}

int potentiometer_read()
{
    int value;

    value = analogRead(pot);

    return value;
}

float get_distance(int TRIG, int ECHO)
{
    long distance, duration;

    digitalWrite(TRIG, LOW);
    digitalWrite(ECHO, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    duration = pulseIn(ECHO1, HIGH);

    if (duration == 0)
        return MAX_DISTANCE;    //no responce
    else
        return distance = ((float)(340 * duration) / 1000) / 2; //speed 340m/s
}

void steering(int steer)
{
    int current_pot = potentiometer_read();
    int steer_pot = map(steer, -90, 90, 677, 277);
    int pot_diff = abs(current_pot - steer_pot);
    int motor_speed = (int)(map(pot_diff, 0, (200), 0, 255)*1.2);
    
    if (current_pot < steer_pot) {
        analogWrite(steer_m1, motor_speed);
        analogWrite(steer_m2, LOW);
    } else if (current_pot > steer_pot) {
        analogWrite(steer_m1, LOW);
        analogWrite(steer_m2, motor_speed);
    } else {
        analogWrite(steer_m1, LOW);
        analogWrite(steer_m2, LOW);
    }
}
/*
void traffic()
{
  if (Serial.available() > 0) {
    char commandT = Serial.read();
    if (commandT == 'H'){  //hold
      hold();
    }
  }
}
*/

void drive()
{
    if (Serial.available() > 0) {
        // Read the command from Python
        char command = Serial.read();
        // Execute the corresponding action
        if (command == '0'){
          //left most
          tok_left(90, 100);
        }
        else if (command == '1'){
          left(90, 130);
        }
        else if (command == '2'){
          left(35, 170);
        }
        else if (command == '3'){
          left(20, 170);
        }
        else if (command == '4'){
          //straight
          straight(170);
        }
        else if (command == '5'){
          right(20, 170);
        }
        else if (command == '6'){
          right(40, 170);
        }
        else if (command == '7'){
          right(90, 130);
        }
        else if (command == '8'){
          //right most
          tok_right(90, 100);
        }
        else {
          //conner case
          hold();
        }
    }
}

void backward_parking(int speed = 60)
{
    int steer_pot = map(0, -90, 90, 686, 286); //Steer_pot = 486
    //int steer_pot = 490;
    //Serial.print("steer_pot:");
    //Serial.println(steer_pot);
    //int current_pot = potentiometer_read();
    //int motor_speed = (int)(map(abs(current_pot - steer_pot), 0, 200, 0, 255)*1.2);

    
    
    while (true) {
        int current_pot = potentiometer_read();
        Serial.print("steer_pot: ");
        Serial.println(steer_pot);
        Serial.print("current_pot: ");
        Serial.println(current_pot);
        
        int motor_speed = (int)(map(abs(current_pot - steer_pot), 0, 240, 0, 255)*1.2);
        Serial.print("motor_speed: ");
        Serial.println(motor_speed);
        int pot_diff = abs(current_pot - steer_pot);
        
        if (current_pot < steer_pot) {
            Serial.println("c<s");

            //current_pot++;
            analogWrite(steer_m1, motor_speed);
            analogWrite(steer_m2, LOW);
            delay(1000);
            
            if (pot_diff <= 10){
              Serial.println("pot_diff < 5");
              //delay(700);
              break;
            }    
        } else if (current_pot > steer_pot) {
            Serial.println("c>s");

            //current_pot--;
            analogWrite(steer_m1, LOW);
            analogWrite(steer_m2, motor_speed);
            delay(1000);
            if (pot_diff <= 10 ){
              Serial.println("pot_diff < 5");
              //delay(700);
              break;
            }            
            
            
        } else {
            Serial.println("almost c=s");
            //int motor_speed = map(current_pot, 0, 180, 0, 255);
            analogWrite(steer_m1, LOW);
            analogWrite(steer_m2, LOW);
            delay(500);
            break;       
        }
    }

    
    
    analogWrite(m1_a, LOW);
    analogWrite(m1_b, speed);
    analogWrite(m2_a, LOW);
    analogWrite(m2_b, speed);
}


void straight_2(int speed = 60)
{
    int steer_pot = map(0, -90, 90, 686, 286); //Steer_pot = 486
    //int steer_pot = 490;
    //Serial.print("steer_pot:");
    //Serial.println(steer_pot);
    //int current_pot = potentiometer_read();
    //int motor_speed = (int)(map(abs(current_pot - steer_pot), 0, 200, 0, 255)*1.2);

    
    
    while (true) {
        int current_pot = potentiometer_read();
        Serial.print("steer_pot: ");
        Serial.println(steer_pot);
        Serial.print("current_pot: ");
        Serial.println(current_pot);
        
        int motor_speed = (int)(map(abs(current_pot - steer_pot), 0, 250, 0, 255)*1.2);
        Serial.print("motor_speed: ");
        Serial.println(motor_speed);
        int pot_diff = abs(current_pot - steer_pot);
        
        if (current_pot < steer_pot) {
            Serial.println("c<s");

            //current_pot++;
            analogWrite(steer_m1, motor_speed);
            analogWrite(steer_m2, LOW);
            delay(1000);
            
            if (pot_diff <= 10){
              Serial.println("pot_diff < 5");
              //delay(700);
              break;
            }    
        } else if (current_pot > steer_pot) {
            Serial.println("c>s");

            //current_pot--;
            analogWrite(steer_m1, LOW);
            analogWrite(steer_m2, motor_speed);
            delay(1000);
            if (pot_diff <= 10 ){
              Serial.println("pot_diff < 5");
              //delay(700);
              break;
            }            
            
            
        } else {
            Serial.println("almost c=s");
            //int motor_speed = map(current_pot, 0, 180, 0, 255);
            analogWrite(steer_m1, LOW);
            analogWrite(steer_m2, LOW);
            delay(500);
            break;       
        }
    }

    
    
    analogWrite(m1_a, speed);
    analogWrite(m1_b, LOW);
    analogWrite(m2_a, speed);
    analogWrite(m2_b, LOW);
}


void straight_parking(int speed = 60)
{
  steering(-30);
  delay(1000);
  hold();
  delay(500);
  straight_2(speed);
  delay(7000);
  //hold();
  //delay(3000);
}

void parking24()
{


  /////////////////
  
  straight_parking(50);

  //right(30, 50);
  //delay(2000);
  //hold();
  //delay(1000);
  
  straight_parking(50);

  //right(30, 50);
  //delay(2000);
  //hold();
  //delay(1000);
  
  straight_parking(50);
  steering(-30);
  delay(1000);
  hold();
  delay(500);
  straight_2(50);
  delay(3000);



  left(20,50);
  delay(8000);
  hold();
  delay(300);

  steering(-30);
  delay(200);

  hold();
  analogWrite(steer_m1, LOW);
  analogWrite(steer_m2, 200);
  delay(500);
  backright(60,80);
  delay(9000);
  
  backward(15);
  delay(1800);

  //steering(-30);
  //delay(200);
  //hold();
  //delay(200);
  //backward_parking(30);
  //delay(6000);

  hold();
  delay(3000);

  ///////////parking complete/////////
  steering(30);
  delay(200);
  hold();
  delay(200);
  
  straight_parking(30);

  left(40,100);
  delay(9000);

  //straight_parking(50);
  straight(50);
  delay(10000);
  
  Serial.println("finish");
  
 
  while(1){
    Serial.println("*********finish*********");
    hold();
  }
      
}

void parking13()
{


  /////////////////
  
  //straight_parking(50);

  //right(30, 50);
  //delay(2000);
  //hold();
  //delay(1000);
  
  straight_parking(50);

  //right(30, 50);
  //delay(2000);
  //hold();
  //delay(1000);
  
  straight_parking(50);
  steering(-40);
  delay(1000);
  hold();
  delay(500);
  straight_2(50);
  delay(4500);



  left(20,50);
  delay(8000);
  hold();
  delay(300);

  steering(-40);
  delay(200);

  hold();
  analogWrite(steer_m1, LOW);
  analogWrite(steer_m2, 200);
  delay(500);
  backright(60,80);
  delay(9000);
  
  backward(15);
  delay(1800);

  //steering(-30);
  //delay(200);
  //hold();
  //delay(200);
  //backward_parking(30);
  //delay(6000);

  hold();
  delay(3000);

  ///////////parking complete/////////
  steering(30);
  delay(200);
  hold();
  delay(200);
  
  straight_parking(30);

  left(40,100);
  delay(9000);

  //straight_parking(50);
  straight(50);
  delay(10000);
  
  Serial.println("finish");
  
 
  while(1){
    Serial.println("*********finish*********");
    hold();
  }
      
}



void avoid(){
  if (get_distance(TRIG2, ECHO2)< 1000){
    Serial.println('afh');
    left(90, 100);
    delay(1000);
    right(90,100);
    delay(1000);
    straight(100);
    delay(500);
    right(90,100);
    delay(700);
    left(90,100);
    delay(200);
  }
}


void setup()
{
    Serial.begin(9600);

    pinMode(m1_a, OUTPUT);
    pinMode(m1_b, OUTPUT);
    pinMode(m2_a, OUTPUT);
    pinMode(m2_b, OUTPUT);
    
    pinMode(steer_m1, OUTPUT);
    pinMode(steer_m2, OUTPUT);
    
    pinMode(ECHO1, INPUT);
    pinMode(TRIG1, OUTPUT);
    pinMode(ECHO2, INPUT);
    pinMode(TRIG2, OUTPUT);
    pinMode(ECHO3, INPUT);
    pinMode(TRIG3, OUTPUT);

    hold();
}

void loop()
{
    if(Serial){
      delay(100);
      Serial.println("Connected");
    }

    
    if (start)
    {
        if (mode == 0){
          drive();
        }
        else if (mode == 1) {
          Serial.println("avoid+traffic mode start");
          avoid();
        }
        else if (mode == 2) {
          Serial.println("parking mode start");
          parking24();
        }
        else if (mode == 3) {
          Serial.println("parking mode start");
          parking13();
        }
        else if (mode == 4) {
          Serial.println("traffic only mode start");
          //traffic();
        }          
    }
    else
    {
        if (Serial.available()>0) { // Check if data is available to read
            
            char key = Serial.read();
            if (key == '0'){    //driving
              start = true;
              mode = 0;
            } else if (key == '1'){   //avoid+traffic
              start = true;
              mode = 1;
            } else if (key == '2'){   //parking24
              start = true;
              mode = 2;
            } else if (key == '3'){   //parking13
              start = true;
              mode = 3; 
            } else if (key == '4'){   //traffic
              start = true;
              mode = 4;
              
            }             
        }
    }
}
