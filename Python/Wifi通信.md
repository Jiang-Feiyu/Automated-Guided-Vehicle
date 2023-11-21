一台电脑作为服务器，另一台作为客户端。在服务器端运行HTTP服务器程序，然后在客户端运行HTTP客户端程序以与服务器通信。
# HTTP 服务器程序
´´´
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
´´´
