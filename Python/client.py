import requests
import serial
import serial.tools.list_ports
import time

# 查找串口号
def find_arduino_port():
    ports = serial.tools.list_ports.grep("1a86:7523")
    for port, desc, hwid in ports:
        return port
    return None

# 向Arduino发送消息
def send_msg_to_Arduino(msg):
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

# 接受server的http请求
def http_rec(server_address):
    # 发送HTTP GET请求
    response = requests.get(server_address)

    # 打印服务器响应
    print("Server Response:")
    print(response.text)

    return response.text

# 向server发送http请求
def http_send(server_address, message):
    # 发送HTTP POST请求，将消息发送给服务器
    response_post = requests.post(server_address, data=message)

    # 打印服务器的响应
    print("Server Response:")
    print(response_post.text)

# 监听轮询
def listen_to_server(server_address):
    while True:
        # 接收服务器请求
        server_response = str(http_rec(server_address))
        print("message recieved from the server:")
        print(server_response)
        
        # 将服务器请求中转到Arduino
        send_msg_to_Arduino(server_response)
        print("message recieved to Arduino")
        
        # 发送用户输入的消息给服务器
        http_send(server_address, "msg received:"+server_response)

        # 休眠一段时间，可以根据实际情况调整
        time.sleep(0.5)

if __name__ == "__main__":
    # 服务器地址和端口
    server_address = 'http://192.168.1.20:8888'  # 请替换为你的服务器地址和端口

    # 启动客户端监听
    listen_to_server(server_address)
