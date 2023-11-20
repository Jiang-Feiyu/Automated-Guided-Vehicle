# Python Code

import serial
import time

# 设置串口参数
ser = serial.Serial('COM3', 9600, timeout=1)

# 向Arduino发送消息
ser.write("This is Python\n".encode('utf-8'))

# 等待一段时间，以确保Arduino有足够的时间处理消息并发送回复
time.sleep(2)

# 读取Arduino的回复
response = ser.readline().decode('utf-8').strip()

# 打印回复消息
print("Arduino says:", response)

# 关闭串口连接
ser.close()
