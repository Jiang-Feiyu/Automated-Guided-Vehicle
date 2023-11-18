import serial
import time

# 蓝牙串口虚拟文件
port = '/dev/rfcomm0'

# 设置蓝牙波特率
bluetooth_serial = serial.Serial(port, 9600)

# 多次发送保证发送成功
for i in range(1, 10):
    # 要发送的数据
    data_to_send = f"Hello, message {i}"

    # 将字符串转换为字节对象并发送
    bluetooth_serial.write(data_to_send.encode('utf-8'))

    # 等待一段时间，确保数据被发送
    time.sleep(1)

# 关闭蓝牙串口连接
bluetooth_serial.close()
