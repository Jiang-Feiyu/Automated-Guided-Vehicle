#define MOTORA_PWM_PIN 3    // 电机A的PWM引脚
#define MOTORA_DIR_PIN1 22
#define MOTORA_DIR_PIN2 23   // 电机A的方向引脚
#define MOTORB_PWM_PIN 4    // 电机B的PWM引脚
#define MOTORB_DIR_PIN1 24
#define MOTORB_DIR_PIN2 25   // 电机B的方向引脚
#define MOTORC_PWM_PIN 5    // 电机C的PWM引脚
#define MOTORC_DIR_PIN1 26
#define MOTORC_DIR_PIN2 27   // 电机C的方向引脚
#define MOTORD_PWM_PIN 6    // 电机D的PWM引脚
#define MOTORD_DIR_PIN1 28   // 电机D的方向引脚
#define MOTORD_DIR_PIN2 29   // 电机D的方向引脚

// 定义电机PWM值
#define Motor_PWM 255

void setup() {
  // 初始化电机引脚
  pinMode(MOTORA_PWM_PIN, OUTPUT);
  pinMode(MOTORA_DIR_PIN1, OUTPUT);
  pinMode(MOTORA_DIR_PIN2, OUTPUT);
  pinMode(MOTORB_PWM_PIN, OUTPUT);
  pinMode(MOTORB_DIR_PIN1, OUTPUT);
  pinMode(MOTORB_DIR_PIN2, OUTPUT);
  pinMode(MOTORC_PWM_PIN, OUTPUT);
  pinMode(MOTORC_DIR_PIN1, OUTPUT);
  pinMode(MOTORC_DIR_PIN2, OUTPUT);
  pinMode(MOTORD_PWM_PIN, OUTPUT);
  pinMode(MOTORD_DIR_PIN1, OUTPUT);
  pinMode(MOTORD_DIR_PIN2, OUTPUT);

  Serial.begin(9600);  // 初始化串口通信，波特率设置为9600
}

void loop() {
  if (Serial.available()) {
    int command = Serial.parseInt();
    executeCommand(command);
  }
}

// 根据接收到的命令执行相应的动作
void executeCommand(int command) {
  switch (command) {
    case 0:  // 静止
      STOP();
      break;
    case 1:  // 前进
      ADVANCE();
      break;
    case 2:  // 后退
      BACK();
      break;
    case 3:  // 左移
      LEFT();
      break;
    case 4:  // 右移
      RIGHT();
      break;
    default:
      break;
  }
}

// 后退
void BACK() {
  MOTORA_BACKOFF(Motor_PWM);
  MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);
  MOTORD_BACKOFF(Motor_PWM);
}

// 前进
void ADVANCE() {
  MOTORA_FORWARD(Motor_PWM);
  MOTORB_FORWARD(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM);
  MOTORD_FORWARD(Motor_PWM);
}

// 左移
void LEFT() {
  MOTORA_STOP(Motor_PWM);
  MOTORB_FORWARD(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);
  MOTORD_STOP(Motor_PWM);
}

// 右移
void RIGHT() {
  MOTORA_FORWARD(Motor_PWM);
  MOTORB_BACKOFF(Motor_PWM);
  MOTORC_STOP(Motor_PWM);
  MOTORD_FORWARD(Motor_PWM);
}

// 停止
void STOP() {
  MOTORA_STOP(Motor_PWM);
  MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);
  MOTORD_STOP(Motor_PWM);
}

// 控制电机A后退
void MOTORA_BACKOFF(uint8_t pwm) {
  digitalWrite(MOTORA_DIR_PIN1, HIGH);
  digitalWrite(MOTORA_DIR_PIN2, LOW);
  analogWrite(MOTORA_PWM_PIN, pwm);
}

// 控制电机A前进
void MOTORA_FORWARD(uint8_t pwm) {
  digitalWrite(MOTORA_DIR_PIN1, LOW);
  digitalWrite(MOTORA_DIR_PIN2, HIGH);
  analogWrite(MOTORA_PWM_PIN, pwm);
}

// 控制电机A停止
void MOTORA_STOP(uint8_t pwm) {
  digitalWrite(MOTORA_DIR_PIN1, LOW);
  digitalWrite(MOTORA_DIR_PIN2, LOW);
  analogWrite(MOTORA_PWM_PIN, pwm);
}

// 控制电机B后退
void MOTORB_BACKOFF(uint8_t pwm) {
  digitalWrite(MOTORB_DIR_PIN1, HIGH);
  digitalWrite(MOTORB_DIR_PIN2, LOW);
  analogWrite(MOTORB_PWM_PIN, pwm);
}

// 控制电机B前进
void MOTORB_FORWARD(uint8_t pwm) {
  digitalWrite(MOTORB_DIR_PIN1, LOW);
  digitalWrite(MOTORB_DIR_PIN2, HIGH);
  analogWrite(MOTORB_PWM_PIN, pwm);
}

// 控制电机B停止
void MOTORB_STOP(uint8_t pwm) {
  digitalWrite(MOTORB_DIR_PIN1, LOW);
  digitalWrite(MOTORB_DIR_PIN2, LOW);
  analogWrite(MOTORB_PWM_PIN, pwm);
}

// 控制电机C后退
void MOTORC_BACKOFF(uint8_t pwm) {
  digitalWrite(MOTORC_DIR_PIN1, HIGH);
  digitalWrite(MOTORC_DIR_PIN2, LOW);
  analogWrite(MOTORC_PWM_PIN, pwm);
}

// 控制电机C前进
void MOTORC_FORWARD(uint8_t pwm) {
  digitalWrite(MOTORC_DIR_PIN1, LOW);
  digitalWrite(MOTORC_DIR_PIN2, HIGH);
  analogWrite(MOTORC_PWM_PIN, pwm);
}

// 控制电机C停止
void MOTORC_STOP(uint8_t pwm) {
  digitalWrite(MOTORC_DIR_PIN1, LOW);
  digitalWrite(MOTORC_DIR_PIN2, LOW);
  analogWrite(MOTORC_PWM_PIN, pwm);
}

// 控制电机D后退
void MOTORD_BACKOFF(uint8_t pwm) {
  digitalWrite(MOTORD_DIR_PIN1, HIGH);
  digitalWrite(MOTORD_DIR_PIN2, LOW);
  analogWrite(MOTORD_PWM_PIN, pwm);
}

// 控制电机D前进
void MOTORD_FORWARD(uint8_t pwm) {
  digitalWrite(MOTORD_DIR_PIN1, LOW);
  digitalWrite(MOTORD_DIR_PIN2, HIGH);
  analogWrite(MOTORD_PWM_PIN, pwm);
}

// 控制电机D停止
void MOTORD_STOP(uint8_t pwm) {
  digitalWrite(MOTORD_DIR_PIN1, LOW);
  digitalWrite(MOTORD_DIR_PIN2, LOW);
  analogWrite(MOTORD_PWM_PIN, pwm);
}
