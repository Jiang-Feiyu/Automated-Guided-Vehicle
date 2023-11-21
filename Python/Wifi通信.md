
# 概述：
- 一台电脑作为服务器，另一台作为客户端。在服务器端运行HTTP服务器程序，然后在客户端运行HTTP客户端程序以与服务器通信。
- 在运行这两个程序之前，请确保两台计算机在同一网络中，并且它们之间可以相互访问。你可以使用一台计算机的IP地址来替换`server_address`中的地址
- 通过`ifconfig`/`ipconfig`（Mac/Windows）查找server的ip地址, 这里将windows作为服务器进行试验
- 通过查找`无线局域网适配器`，获得ip地址
    ```
    无线局域网适配器 WLAN:

       连接特定的 DNS 后缀 . . . . . . . :
       IPv4 地址 . . . . . . . . . . . . : 192.168.1.20
       子网掩码  . . . . . . . . . . . . : 255.255.255.0
       默认网关. . . . . . . . . . . . . : 192.168.1.1
    ```
    我们选择无线局域网适配器的IPv4地址作为服务器地址
- 注意
    - 不要挂VPN
    - 如果显示端口被占用，如：`OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。`那么就更换一个port
    - 先启动server，再启动client
# 示例代码
## HTTP 服务器程序
```
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

# 指定服务器地址和端口
host = '0.0.0.0'  # 可以是具体的IP地址，也可以是0.0.0.0表示接受任何可用的网络接口
port = 8888

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
server_address = 'http://192.168.1.20:8888'  # 请替换为你的服务器地址和端口

# 发送HTTP GET请求
response = requests.get(server_address)

# 打印服务器响应
print("Server Response:")
print(response.text)
```
运行结果：
</br> server端运行结果： 
<p align=center><img src="https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4a438ed12aa848d4b38fed2e3de32056~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=595&h=67&s=6861&e=png&b=181818" alt="屏幕截图 2023-11-21 234041.png" width="70%" /></p>
</br> client端运行结果：
<p align=center><img src="https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b5236dd5722649f1ad14fcac5b31a9b4~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2144&h=1048&s=195607&e=png&b=181818" alt="螢幕截圖 2023-11-21 下午11.42.57.png" width="70%" /></p>
