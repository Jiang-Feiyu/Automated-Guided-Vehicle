
# 概述：
- 一台电脑作为服务器，另一台作为客户端。在服务器端运行HTTP服务器程序，然后在客户端运行HTTP客户端程序以与服务器通信。
- 在运行这两个程序之前，请确保两台计算机在同一网络中，并且它们之间可以相互访问。你可以使用一台计算机的IP地址来替换`server_address`中的地址
# 示例代码
## HTTP 服务器程序
```
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
# 指定服务器地址和端口
host = '0.0.0.0'  # 可以是具体的IP地址，也可以是0.0.0.0表示接受任何可用的网络接口
port = 8080

# 设置服务器
server_address = (host, port)
httpd = TCPServer(server_address, SimpleHTTPRequestHandler)

# 打印服务器信息
print(f"Serving on {host}:{port}")

# 启动服务器
httpd.serve_forever()
```
## HTTP 客户端程序
```
import requests

# 服务器地址和端口
server_address = 'http://192.168.1.100:8080'  # 请替换为你的服务器地址和端口

# 发送HTTP GET请求
response = requests.get(server_address)

# 打印服务器响应
print("Server Response:")
print(response.text)
```
