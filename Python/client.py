import requests
import time

def send_message_to_server(server_address, message):
    # 发送HTTP POST请求，将消息发送给服务器
    response_post = requests.post(server_address, data=message)

    # 打印服务器的响应
    print("Server Response:")
    print(response_post.text)

def listen_to_server(server_address):
    while True:
        # 获取用户输入的消息
        message_to_server = input("Enter your message to the server: ")

        # 发送HTTP POST请求，将用户输入的消息发送给服务器
        send_message_to_server(server_address, message_to_server)

        # 发送HTTP GET请求
        response = requests.get(server_address)

        # 打印服务器响应
        print("Server Response:")
        print(response.text)

        # 休眠一段时间，可以根据实际情况调整
        time.sleep(5)

if __name__ == "__main__":
    # 服务器地址和端口
    server_address = 'http://192.168.1.20:8888'  # 请替换为你的服务器地址和端口

    # 启动客户端监听
    listen_to_server(server_address)
