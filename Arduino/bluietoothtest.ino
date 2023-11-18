#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX

bool matchingInProgress = false;

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);

  Serial.println("Bluetooth检测程序");

  // 等待蓝牙模块初始化
  delay(1000);
}

void loop() {
  if (mySerial.available()) {
    char receivedChar = mySerial.read();

    if (receivedChar == 'A') {
      if (!matchingInProgress) {
        matchingInProgress = true;
        Serial.println("匹配中...");
        delay(2000);  // 等待2秒钟（可以根据需要调整等待时间）
      }
    } else if (receivedChar == 'B') {
      if (matchingInProgress) {
        matchingInProgress = false;
        Serial.println("匹配成功！");
      }
    } else {
      if (matchingInProgress) {
        Serial.println("未知状态");
      }
    }
  }
}
