import serial
import serial.tools.list_ports
import time
from flask import Flask, request

app = Flask(__name__)

# 查找串口号
def find_arduino_port():
    ports = serial.tools.list_ports.grep("1a86:7523")
    for port, desc, hwid in ports:
        return port
    return None

# 信息发送
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
                time.sleep(3)

                # 读取Arduino的回复
                res=ser.readline()
                if (res):
                   # 打印回复消息
                    response_str = res.decode('utf-8')
                    print("res:", response_str)
                    tag = 1
                else:
                    print("no response yet")
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        finally:
            # 关闭串口连接
            ser.close()
    else:
        print("Arduino not found.")

def process_client_data():
    received_data = request.form.get('message')
    print("Received from client:", received_data)
    if received_data == "wake up":
        send_msg("2")
    elif received_data == "stop":
        send_msg("0")
    response_to_client = "Message received by server"
    return response_to_client

# 定义路由，处理GET和POST请求
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 处理客户端的GET请求
        return "Server is ready to receive messages"
    elif request.method == 'POST':
        # 处理客户端的POST请求，调用封装的函数
        return process_client_data()

if __name__ == '__main__':
    # 运行Flask应用
    app.run(host='0.0.0.0', port=8888)
