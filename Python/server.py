from flask import Flask, request

app = Flask(__name__)

# 定义路由，处理GET和POST请求
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 处理客户端的GET请求
        return "Server is ready to receive messages"
    elif request.method == 'POST':
        # 处理客户端的POST请求
        received_data = request.data.decode('utf-8')
        print("Received from client:", received_data)

        # 回应客户端
        response_to_client = "Message received by server"
        return response_to_client

if __name__ == '__main__':
    # 运行Flask应用
    app.run(host='0.0.0.0', port=8888)
