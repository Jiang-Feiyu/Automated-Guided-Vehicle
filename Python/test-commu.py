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
            ser = serial.Serial(arduino_port, 9600, timeout=1)
            print("ser.is_open")

            # 向Arduino发送消息
            tag = 0
            while (tag == 0):
                print("msg sent", msg)
                ser.write(msg.encode('utf-8'))

                # 等待一段时间，以确保Arduino有足够的时间处理消息并发送回复
                time.sleep(2)

                # 读取Arduino的回复
                response = ser.readline().decode('utf-8').strip()

                # 打印回复消息
                print("res:", response)
                tag = 1
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        finally:
            # 关闭串口连接
            ser.close()
    else:
        print("Arduino not found.")

for i in range(0, 5):
    send_msg(str(i)+":move")
