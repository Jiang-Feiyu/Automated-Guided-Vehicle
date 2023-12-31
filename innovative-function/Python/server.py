import serial
import serial.tools.list_ports
import time
from flask import Flask, request

status = 0 #标志是否启动
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

# 导航程序
def navigate_to_point(center_x, center_y, yellow_x, yellow_y):
    # 移动方向： 
    # 0 -> stop 
    # 1 -> up 
    # 2 -> down 
    # 3 -> left 
    # 4 -> right 
    tol = 50
    # Calculate the differences in x and y coordinates
    dx = int(yellow_x) - int(center_x)
    dy = int(yellow_y) - int(center_y)
    # if yellow item not found
    if int(yellow_x) == 0 or int(yellow_x) == 0:
        send_msg("0")
    else:
        # Check whether to move up, down, left, or right
        if abs(dx) <= tol and abs(dy) <= tol:
            # Stop if the target is reached
            send_msg("0")
        else:
            # only move y
            if abs(dx) <= tol:
                if dy < 0:
                    # move back
                    send_msg("2")
                else:
                    send_msg("1")
            # only move x
            elif abs(dy) <= tol:
                if dx < 0:
                    # move left
                    send_msg("3")
                else:
                    send_msg("4")
            # move x and y at same time
            else:
                if dx < 0:
                    if dy < 0:
                        send_msg("2")
                        send_msg("3")
                    else:
                        send_msg("1")
                        send_msg("3")
                else:
                    if dy < 0:
                        send_msg("2")
                        send_msg("4")
                    else:
                        send_msg("1")
                        send_msg("4")
                        

# 数据处理
def process_client_data():
    global status
    received_data = request.form.get('message')
    print("Received from client:", received_data)
    if received_data == "":
        print("No Msg")
        response_to_client = "Message received by server"
        return response_to_client
    if received_data == "wake up":
        status = 1
        send_msg("1")
    elif received_data == "stop"  and status == 1:
        send_msg("0")
        status = 0
    elif received_data == "1"  and status == 1:
        send_msg("1")
    elif received_data == "2"  and status == 1:
        send_msg("2")
    elif received_data == "3"  and status == 1:
        send_msg("3")
    elif received_data == "4"  and status == 1:
        send_msg("4")
    else:
        if status == 1:
            center_x, center_y, yellow_x, yellow_y = received_data.split(" ")
            navigate_to_point(center_x, center_y, yellow_x, yellow_y)
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
