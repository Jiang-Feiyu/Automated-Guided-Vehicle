/*
This is the code of E12 Group Project
*/

#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <SoftwareSerial.h>
#include <Servo.h>
#include <INA226.h>

#define MOTORA_FORWARD(pwm)    do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,HIGH);analogWrite(PWMA,pwm);}while(0)
#define MOTORA_STOP(x)         do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,LOW); analogWrite(PWMA,0);}while(0)
#define MOTORA_BACKOFF(pwm)    do{digitalWrite(DIRA1,HIGH);digitalWrite(DIRA2,LOW); analogWrite(PWMA,pwm);}while(0)

#define MOTORB_FORWARD(pwm)    do{digitalWrite(DIRB1,LOW); digitalWrite(DIRB2,HIGH);analogWrite(PWMB,pwm);}while(0)
#define MOTORB_STOP(x)         do{digitalWrite(DIRB1,LOW); digitalWrite(DIRB2,LOW); analogWrite(PWMB,0);}while(0)
#define MOTORB_BACKOFF(pwm)    do{digitalWrite(DIRB1,HIGH);digitalWrite(DIRB2,LOW); analogWrite(PWMB,pwm);}while(0)

#define MOTORC_FORWARD(pwm)    do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,HIGH);analogWrite(PWMC,pwm);}while(0)
#define MOTORC_STOP(x)         do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,LOW); analogWrite(PWMC,0);}while(0)
#define MOTORC_BACKOFF(pwm)    do{digitalWrite(DIRC1,HIGH);digitalWrite(DIRC2,LOW); analogWrite(PWMC,pwm);}while(0)

#define MOTORD_FORWARD(pwm)    do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,HIGH);analogWrite(PWMD,pwm);}while(0)
#define MOTORD_STOP(x)         do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,LOW); analogWrite(PWMD,0);}while(0)
#define MOTORD_BACKOFF(pwm)    do{digitalWrite(DIRD1,HIGH);digitalWrite(DIRD2,LOW); analogWrite(PWMD,pwm);}while(0)

#define SERIAL  Serial
#define BTSERIAL Serial3

#define LOG_DEBUG

#ifdef LOG_DEBUG
  #define M_LOG SERIAL.print
#else
  #define M_LOG BTSERIAL.println
#endif

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     28 //4 // Reset pin # (or -1 if sharing Arduino reset pin)

// Define motor pins
#define PWMA 12    //Motor A PWM
#define DIRA1 34
#define DIRA2 35  //Motor A Direction
#define PWMB 8    //Motor B PWM
#define DIRB1 37
#define DIRB2 36  //Motor B Direction
#define PWMC 6   //Motor C PWM
#define DIRC1 43
#define DIRC2 42  //Motor C Direction
#define PWMD 5    //Motor D PWM
#define DIRD1 A4  //26  
#define DIRD2 A5  //27  //Motor D Direction

//PWM Definition
#define MAX_PWM   2000
#define MIN_PWM   300
#define SERVO_PIN 9        //servo connected at pin 9
#define TOL   2           //tolerance for adc different, avoid oscillation
#define K   5              //Step size

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
int oldV=1, newV=0;
int pan = 90;
int tilt = 120;
int window_size = 0;
int BT_alive_cnt = 0;
int voltCount = 0;

Servo servo_pan;
Servo servo_tilt;
int servo_min = 20;
int servo_max = 160;

unsigned long time;

//FaBoPWM faboPWM;
int pos = 0;
int MAX_VALUE = 2000;
int MIN_VALUE = 300;

// Servo Definition
Servo myservo;            //declare servo object
int int_position=90;      //Servo initial position

//variables for light intensity to ADC reading equations 
float int_adc0, int_adc0_m, int_adc0_c;
float int_adc1, int_adc1_m, int_adc1_c;     
float int_left, int_right;

int Motor_PWM = 1900;
float power = 0;

// Setting power sensor
INA226 ina;

/* 
Here are functions of movement
*/

void BACK(uint8_t pwm_A, uint8_t pwm_B, uint8_t pwm_C, uint8_t pwm_D)
{
  MOTORA_BACKOFF(Motor_PWM); //    ↑A-----B↑
  MOTORB_FORWARD(Motor_PWM); //     |  ↑  |
  MOTORC_BACKOFF(Motor_PWM); //     |  |  |
  MOTORD_FORWARD(Motor_PWM); //    ↑C-----D↑
}

void ADVANCE()
{
  MOTORA_FORWARD(Motor_PWM); //    ↓A-----B↓
  MOTORB_BACKOFF(Motor_PWM); //     |  |  |
  MOTORC_FORWARD(Motor_PWM); //     |  ↓  |
  MOTORD_BACKOFF(Motor_PWM); //    ↓C-----D↓
}

void LEFT_1()
{
  MOTORA_STOP(Motor_PWM);   //    =A-----B↑
  MOTORB_FORWARD(Motor_PWM);//     |   ↖ |
  MOTORC_BACKOFF(Motor_PWM);//     | ↖   |
  MOTORD_STOP(Motor_PWM);   //    ↑C-----D=
}

void RIGHT_2()
{
  MOTORA_FORWARD(Motor_PWM); //    ↓A-----B↑
  MOTORB_FORWARD(Motor_PWM); //     |  ←  |
  MOTORC_BACKOFF(Motor_PWM); //     |  ←  |
  MOTORD_BACKOFF(Motor_PWM); //    ↑C-----D↓
}

void LEFT_3()
{
  MOTORA_FORWARD(Motor_PWM); //    ↓A-----B=
  MOTORB_STOP(Motor_PWM);    //     | ↙   |
  MOTORC_STOP(Motor_PWM);    //     |   ↙ |
  MOTORD_BACKOFF(Motor_PWM); //    =C-----D↓
}

void RIGHT_1()
{
  MOTORA_BACKOFF(Motor_PWM); //    ↑A-----B=
  MOTORB_STOP(Motor_PWM);    //     | ↗   |
  MOTORC_STOP(Motor_PWM);    //     |   ↗ |
  MOTORD_FORWARD(Motor_PWM); //    =C-----D↑
}

void LEFT_2()
{
  MOTORA_BACKOFF(Motor_PWM); //    ↑A-----B↓
  MOTORB_BACKOFF(Motor_PWM); //     |  →  |
  MOTORC_FORWARD(Motor_PWM); //     |  →  |
  MOTORD_FORWARD(Motor_PWM); //    ↓C-----D↑
}

void RIGHT_3()
{
  MOTORA_STOP(Motor_PWM);    //    =A-----B↓
  MOTORB_BACKOFF(Motor_PWM); //     |   ↘ |
  MOTORC_FORWARD(Motor_PWM); //     | ↘   |
  MOTORD_STOP(Motor_PWM);    //    ↓C-----D=
}

void rotate_1()  //tate_1(uint8_t pwm_A,uint8_t pwm_B,uint8_t pwm_C,uint8_t pwm_D)
{
  MOTORA_BACKOFF(Motor_PWM); //    ↑A-----B↓
  MOTORB_BACKOFF(Motor_PWM); //     | ↗ ↘ |
  MOTORC_BACKOFF(Motor_PWM); //     | ↖ ↙ |
  MOTORD_BACKOFF(Motor_PWM); //    ↑C-----D↓
}

void rotate_2()  // rotate_2(uint8_t pwm_A,uint8_t pwm_B,uint8_t pwm_C,uint8_t pwm_D)
{
  MOTORA_FORWARD(Motor_PWM); //    ↓A-----B↑
  MOTORB_FORWARD(Motor_PWM); //     | ↙ ↖ |
  MOTORC_FORWARD(Motor_PWM); //     | ↘ ↗ |
  MOTORD_FORWARD(Motor_PWM); //    ↓C-----D↑
}

void STOP()
{
  MOTORA_STOP(Motor_PWM); //    =A-----B=
  MOTORB_STOP(Motor_PWM); //     |  =  |
  MOTORC_STOP(Motor_PWM); //     |  =  |
  MOTORD_STOP(Motor_PWM); //    =C-----D=
}

// This function is used to output the voltage, current and power of the solar panel
void UART_Control()
{

}

/*Voltage Readings transmitter
Sends them via Serial3*/
void sendVolt(){
    newV = analogRead(A0);
    if(newV!=oldV) {
      if (!Serial3.available()) {
        Serial3.println(newV);
        Serial.println(newV);
      }
    }
    oldV=newV;
}

// This function is to detect the direction of the car
void tracker()
{
 // If left sensor is brighter than right sensor, decrease servo angle and turn LEFT
  if (int_left>(int_right+TOL))
  {
      Serial.println("left1t");
      LEFT_1();
  }

 // if right sensor is brighter than left sensor, increase servo angle and turn RIGHT
  if (int_left<(int_right-TOL))
  {
      Serial.println("right1");
      RIGHT_1();
  }

  // if right sensor is nearly the same, stop the car
  if ((int_left>(int_right-TOL))&& ((int_left<(int_right+TOL))))
  {
      Serial.println("stop");
      STOP();
  }
}

// This is the function for printing the power
void checkConfig()
{
  Serial.print("Mode:                  ");
  switch (ina.getMode())
  {
    case INA226_MODE_POWER_DOWN:      Serial.println("Power-Down"); break;
    case INA226_MODE_SHUNT_TRIG:      Serial.println("Shunt Voltage, Triggered"); break;
    case INA226_MODE_BUS_TRIG:        Serial.println("Bus Voltage, Triggered"); break;
    case INA226_MODE_SHUNT_BUS_TRIG:  Serial.println("Shunt and Bus, Triggered"); break;
    case INA226_MODE_ADC_OFF:         Serial.println("ADC Off"); break;
    case INA226_MODE_SHUNT_CONT:      Serial.println("Shunt Voltage, Continuous"); break;
    case INA226_MODE_BUS_CONT:        Serial.println("Bus Voltage, Continuous"); break;
    case INA226_MODE_SHUNT_BUS_CONT:  Serial.println("Shunt and Bus, Continuous"); break;
    default: Serial.println("unknown");
  }
  
  Serial.print("Samples average:       ");
  switch (ina.getAverages())
  {
    case INA226_AVERAGES_1:           Serial.println("1 sample"); break;
    case INA226_AVERAGES_4:           Serial.println("4 samples"); break;
    case INA226_AVERAGES_16:          Serial.println("16 samples"); break;
    case INA226_AVERAGES_64:          Serial.println("64 samples"); break;
    case INA226_AVERAGES_128:         Serial.println("128 samples"); break;
    case INA226_AVERAGES_256:         Serial.println("256 samples"); break;
    case INA226_AVERAGES_512:         Serial.println("512 samples"); break;
    case INA226_AVERAGES_1024:        Serial.println("1024 samples"); break;
    default: Serial.println("unknown");
  }

  Serial.print("Bus conversion time:   ");
  switch (ina.getBusConversionTime())
  {
    case INA226_BUS_CONV_TIME_140US:  Serial.println("140uS"); break;
    case INA226_BUS_CONV_TIME_204US:  Serial.println("204uS"); break;
    case INA226_BUS_CONV_TIME_332US:  Serial.println("332uS"); break;
    case INA226_BUS_CONV_TIME_588US:  Serial.println("558uS"); break;
    case INA226_BUS_CONV_TIME_1100US: Serial.println("1.100ms"); break;
    case INA226_BUS_CONV_TIME_2116US: Serial.println("2.116ms"); break;
    case INA226_BUS_CONV_TIME_4156US: Serial.println("4.156ms"); break;
    case INA226_BUS_CONV_TIME_8244US: Serial.println("8.244ms"); break;
    default: Serial.println("unknown");
  }

  Serial.print("Shunt conversion time: ");
  switch (ina.getShuntConversionTime())
  {
    case INA226_SHUNT_CONV_TIME_140US:  Serial.println("140uS"); break;
    case INA226_SHUNT_CONV_TIME_204US:  Serial.println("204uS"); break;
    case INA226_SHUNT_CONV_TIME_332US:  Serial.println("332uS"); break;
    case INA226_SHUNT_CONV_TIME_588US:  Serial.println("558uS"); break;
    case INA226_SHUNT_CONV_TIME_1100US: Serial.println("1.100ms"); break;
    case INA226_SHUNT_CONV_TIME_2116US: Serial.println("2.116ms"); break;
    case INA226_SHUNT_CONV_TIME_4156US: Serial.println("4.156ms"); break;
    case INA226_SHUNT_CONV_TIME_8244US: Serial.println("8.244ms"); break;
    default: Serial.println("unknown");
  }
  
  Serial.print("Max possible current:  ");
  Serial.print(ina.getMaxPossibleCurrent());
  Serial.println(" A");

  Serial.print("Max current:           ");
  Serial.print(ina.getMaxCurrent());
  Serial.println(" A");

  Serial.print("Max shunt voltage:     ");
  Serial.print(ina.getMaxShuntVoltage());
  Serial.println(" V");

  Serial.print("Max power:             ");
  Serial.print(ina.getMaxPower());
  Serial.println(" W");
}


//Where the program starts
void setup()
{
  SERIAL.begin(115200); // USB serial setup

  // Servo connection
  myservo.attach(SERVO_PIN);
  myservo.write(int_position);
  delay(500); 

  // Process data from light sensor
  int_adc0=analogRead(A0);   // Left sensor at ambient light intensity
  int_adc1=analogRead(A1);   // Right sensor at ambient light intensity

  // measure the sensors reading at zero light intensity  
  int_adc0_c=245;   // Left sensor at zero light intensity
  int_adc1_c=475;   // Right sensor at zero light intensity

  // calculate the slope of light intensity to ADC reading equations  
  int_adc0_m=(int_adc0-int_adc0_c)/100;
  int_adc1_m=(int_adc1-int_adc1_c)/100;

  // Initialize the parameters of the car
  SERIAL.println("Start");
  STOP(); 
  servo_pan.attach(48);
  servo_tilt.attach(47);

  //Setup Voltage detector
  pinMode(A0, INPUT);

  //Setup the power sensor
  // Default INA226 address is 0x40
  ina.begin();
  ina.configure(INA226_AVERAGES_16, INA226_BUS_CONV_TIME_2116US, INA226_SHUNT_CONV_TIME_2116US, INA226_MODE_SHUNT_BUS_CONT);
  ina.calibrate(0.0015, 4);
  checkConfig();

  // OLED setup
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
  }
  display.clearDisplay();
  display.setTextSize(2);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.cp437(true);         // Use full 256 char 'Code Page 437' font
  display.setCursor(0, 0);     // Start at top-left corner
  display.println("Power");
  display.display();
}

void loop(){
  // run the code in every 20ms
  if (millis() > (time + 15)) {
    voltCount++;
    time = millis();

    //constrain the servo movement
    pan = constrain(pan, servo_min, servo_max);
    tilt = constrain(tilt, servo_min, servo_max);
    
    //send signal to servo
    servo_pan.write(pan);
    servo_tilt.write(tilt);
  }if (voltCount>=5){
    voltCount=0;
    sendVolt();
  }

  // Movement control
  if (ina.readBusPower() <= power) {
    float busPower = ina.readBusPower();
    Serial.println("power: " + String(busPower) + " ADVANCE");
    power = ina.readBusPower();
    ADVANCE();

    // 在OLED上显示power的值
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Power: " + String(power) + " W");
    display.display();
  } else {
    float busPower = ina.readBusPower();
    Serial.println("power: " + String(busPower) + " BACK");
    power = ina.readBusPower();
    STOP();

    // 在OLED上显示power的值
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Power: " + String(power) + " W");
    display.display();
  }

  // direction control
  int_left=(analogRead(A0)-int_adc0_c)/int_adc0_m;
  int_right=(analogRead(A1)-int_adc1_c)/int_adc1_m; 
  Serial.println("int_left: " + String(int_left) + " analogRead(A0): " + String(analogRead(A0)) + " int_adc0_c: " + String(int_adc0_c) + " int_adc0_m: " + String(int_adc0_m));
  Serial.println("int_right: " + String(int_right) + " analogRead(A1): " + String(analogRead(A1)) + " int_adc1_c: " + String(int_adc1_c) + " int_adc1_m: " + String(int_adc1_m));
  Serial.println();
  tracker();

  // Print the power on LED

}
