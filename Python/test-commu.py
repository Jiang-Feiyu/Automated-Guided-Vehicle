import serial
import serial.tools.list_ports
import time

# 查找串口号
def find_arduino_port():
    ports = serial.tools.list_ports.grep("1a86:7523")
    for port, desc, hwid in ports:
        return port
    return None

def send_msg(msg):
    # 查找Arduino串口号
    arduino_port = find_arduino_port()
    print("arduino_port:", arduino_port)

    if arduino_port:
        try:
            # 设置串口参数并打开串口
            ser = serial.Serial(arduino_port, 9600, timeout=1)
            print("Serial name:", ser.name)
            print("Serial baudrate:", ser.baudrate)
            print("Serial state:", ser.is_open)

            # 向Arduino发送消息
            print("msg sent")
            ser.write(msg.encode('utf-8'))

            # 读取Arduino的回复
            response = ser.readline().decode('utf-8').strip()

            # 打印回复消息
            print("res:", response)

            # 等待一段时间，以确保Arduino有足够的时间处理消息并发送回复
            time.sleep(2)

        except serial.SerialException as e:
            print(f"Serial error: {e}")

        finally:
            # 关闭串口连接
            ser.close()
    else:
        print("Arduino not found.")

for i in range(0, 5):
    send_msg(i)
