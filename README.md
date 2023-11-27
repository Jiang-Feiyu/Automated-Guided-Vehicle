# ELEC3848_gp
## Group E12
<p align=center><img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6d9e1938da4f4fa1a48c00fd7f5f4772~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2012&h=1170&s=445844&e=jpg&b=cac4b9" alt="IMG_5337.jpg" width="70%" /></p>
<p align=center><img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7a45047f4d9e4c99bcbc168029592e6f~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1170&h=626&s=159325&e=jpg&b=b9c1bf" alt="IMG_5338.jpg" width="70%" /></p>
<p align=center><img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/de7117270da9458f993b2d50b933344e~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1170&h=629&s=377610&e=jpg&b=8b867e" alt="IMG_5339.jpg" width="70%" /></p>

## Overall
### Document tree
```
.
├── LICENSE
├── README.md
├── documents
│   ├── Proposal.pdf
│   ├── project description.pdf
│   └── required-function.pdf
├── innovative-function
│   ├── Arduino
│   │   └── move_control.ino
│   ├── Python
│   │   ├── itemRecog.py
│   │   └── server.py
│   └── remote-contrl
│       ├── 1.avif
│       └── start.html
├── required-function
│   ├── Car_Volt_Feedback.ino
│   ├── car.apk
│   └── gp-light.ino
└── tree.txt
```
### Data flow of our project
```mermaid
graph LR
A(Camera) --> B(PC)
C(Frontend Web) --http---> D{Raspberry Pi}
B(PC) --http---> D{Raspberry Pi}
D(Raspberry Pi)--Physical Serial ---> E[Arduino Mega2560]
```
-   **Camera**: Using OpenCV to collect data and send the frames to the PC for model inference.
-   **PC**: Analyzing data and sending the coordinates of the car and suspicious items to the Raspberry Pi for further analysis.
-   **Frontend Web Page**: This serves as the remote control for workers to remotely activate and stop the car (Arduino).
-   **Raspberry Pi**: It continuously listens to the client for commands to wake up or stop. Once awakened, it receives data from the PC to calculate the car's route and sends instructions to Arduino through the physical serial port.
-   **Arduino Mega2560**: Receives data from the Raspberry Pi and moves according to the instructions.
## Item Recognition with OpenCV
<p align=center><img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d1db370e63064cffb77ec3004ca30896~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=852&h=478&s=753204&e=png&b=95938c" alt="螢幕截圖 2023-11-24 下午10.57.53.png" width="70%" /></p>

<p align=center><img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/931e3e363dfa45ca9da0ea0ee4826601~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=421&h=248&s=204408&e=png&b=bfbeb5" alt="螢幕截圖 2023-11-24 下午10.58.03.png" width="70%" /></p>

### Environment setting
It is recommended to create a virtual environment with **Conda** and run the program in the virtual environment.
Here are some steps for reference: (suppose you already have `conda`)
1.  Check environment: `conda env list`
2.  Create a new environment (here is): 
    `conda create -n py36tqrcode numpy pandas python=3.9
    `This command creates a new environment called `py36tqrcode` in the conda environment and installs the Python 3.9, NumPy, and Pandas packages in that environment.
4.  Activate the environment, eg: `conda activate py36tqrcode`
5.  Deactive the environment: `conda deactivate`
6. Please make sure that your Python interpreter is corresponding to your python environment. eg: `conda env list`, then run the program.
### Import the required libraries
The code imports the necessary libraries for image processing, numerical computations, time operations, and sending HTTP requests. 
```
import cv2 
import numpy as np 
import time import requests
```
### Define the object detection function
This function takes a frame (image) as input and performs object detection using color thresholds.
def detect_object(frame):
1. Convert the frame to the HSV color space, creates masks based on pre-defined red and yellow thresholds:
    ```
    # Convert BGR to HSV
    # Define the range of color in HSV
    # Threshold the HSV image to get only specific colors
    ```
2. Find the largest contours in each mask:
3. Draw bounding boxes around the objects, calculate the center coordinates of the objects, and print them.
4. Send the coordinate through http request
    ```
    response_post = requests.post(server_address, data={'message': message})
    ```
    Check if the request was successful (status code 200)
    ```
    if response_post.status_code == 200: 
        print("Server Response:") 
        print(response_post.text) 
    else: 
        print(f"Error: Server returned status code {response_post.status_code}")
    ```
5. Optimizer
   - detection_interval setting:
       ```
       detection_interval = n  # Run detection every 10 frames

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()

            frame_count += 1

            if frame_count % detection_interval == 0:
                center_x, center_y, yellow_x, yellow_y = detect_object(frame)
       ```
    - setting the image pixel
       ```
       frame = cv2.resize(frame, (854, 480))
       ```
## Communication
### Serial communication [1]
1. Raspverry Side
    1. Install necessary python packages: `sudo apt-get install python-serial` and `sudo apt-get install arduino`.
    2. Check the usb devices connected to Raspberry Pi: `lsusb`to search for connection information and check whether the port exists.
        ```
        def find_arduino_port():
            ports = serial.tools.list_ports.grep("1a86:7523")
            for port, desc, hwid in ports:
                return port
            return None
        ```
    3. If the port does exists, then need to try to send and receive messages. A sample code is like:
        ```
        try: 
            while 1: 
                res=ser.readline() #read in data and print 
                print(res) #send the data
                time.sleep(1) 
                ser.write("Hello! I am Raspberry!".encode("utf-8"))
        except: 
            ser.close()
        ```
    4. However, since Raspberry Pi need keep sending command to Arduino, we need to add a tag outside like:
        ```
        if arduino_port:
        try:
            # send data to Arduino
            tag = 0
            while (tag == 0):
               # wait for a while, to make sure Arduino have enough time to process data & reply
                # read in Arduino reply
                res=ser.readline()
                if (res):
                   # print reply
                    tag = 1
                else:
                    print("no response yet")
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        finally:
            # close
        ```
    5. Make sure Arduino and Raspberry are in the same baud rate and the frequency of sending and receieving data should be carefully considered.
    6. Arduino
        ```
        void waitForPythonMessage() {
          String str = "";
          while (Serial.available()) {
            char ch = Serial.read();
            str += ch;
            delay(10);
          }
          if (str.length() > 0) {
              // command that received
              processCommand(str);
              // send response to Python
              sendResponseToPython("Message received!");
            }
         }
        ```
3. Python msg send function: `send_msg("("+str(i)+")")`, plz be aware that the string must be included in the bracket since Arduino read data character by character.

### HTTP Communication in the Same WLAN
#### Basic http function
- One computer serves as the server, while another functions as the client. Run an HTTP server program on the server side and then execute an HTTP client program on the client side to facilitate communication with the server.
- Before running these two programs, ensure that both computers are on the same network and can access each other. You can use the IP address of one computer to replace the address in server_address.
- Find the server's IP address by using ifconfig/ipconfig (Mac/Windows). In this case, we are using Windows as the server.
- Obtain the IP address by searching for "Wireless LAN Adapter".
    ```
    Wireless LAN adapter WLAN:
    Connection specific DNS suffix . . . : 
    IPv4 address. . . . . . . . . . . . .: 192.168.1.20 
    Subnet mask  . . . . . . . . . . . . : 255.255.255.0 
    Default gateway. . . . . . . . . . . : 192.168.1.1
    ```
    Replace the IP address in the WLAN section
- Attention
    - No VPN
    - For errors like `OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。`means port are not available.
    - Start the Server first, then the client
- Sample
    HTTP Server
    ```
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer

    # Specify server address and port
    host = '0.0.0.0'  # Can be a specific IP address, or 0.0.0.0 to accept any available network interface
    port = 8888

    # Set up server
    server_address = (host, port)
    httpd = TCPServer(server_address, SimpleHTTPRequestHandler)

    # Print server information
    print(f"Serving on {host}:{port}")

    # Start the server
    httpd.serve_forever()
    ```
- HTTP Client
    ```
    import requests

    # Server address and port
    server_address = 'http://192.168.1.20:8888' 

    # Send HTTP GET request
    response = requests.get(server_address)

    # Print server response
    print("Server Response:")
    print(response.text)
    ```
- Running result (sample)：
    </br> server： 
    <p align=center><img src="https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4a438ed12aa848d4b38fed2e3de32056~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=595&h=67&s=6861&e=png&b=181818" alt="屏幕截图 2023-11-21 234041.png" width="90%" /></p>
    </br> client：
    <p align=center><img src="https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b5236dd5722649f1ad14fcac5b31a9b4~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2144&h=1048&s=195607&e=png&b=181818" alt="螢幕截圖 2023-11-21 下午11.42.57.png" width="90%" /></p>

#### **Server Side**: Flask

   Our server is designed based on Python `Flask`, all the request from client should be `POST` request, the `process_client_data` function will read and send the specific message to Arduino.  
   
    def process_client_data():
        received_data = request.form.get('message')
        print("Received from client:", received_data)
        # hand the received_data through content
        response_to_client = "Message received by server"
        return response_to_client
        
    # Define routes and handle GET and POST requests
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            # Handle client's GET request
            return "Server is ready to receive messages"
        elif request.method == 'POST':
            # Process the client's POST request and call the encapsulated function
            return process_client_data()

#### Frontend: Remote control

<p align=center><img src="https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9cc9a95714ef49ddaa5709580b6e170d~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1172&h=733&s=641361&e=png&b=150646" alt="螢幕截圖 2023-11-24 下午11.10.53.png" width="70%" /></p>

<p align=center><img src="https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5db5a15cab44428a8794296e1473b1d6~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1165&h=739&s=643483&e=png&b=140645" alt="螢幕截圖 2023-11-24 下午11.11.00.png" width="70%" /></p>

The request sent from the front-end web page is through Javascript:
```
fetch(serverAddress, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'message=' + message,
            })
                .then(response => response.text())
                .then(data => {
                    console.log('Server Response:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
```
The request will be sent as the click-button event is triggered.
## Navigation
This part need to be improved through `pid`:
```
def navigate_to_point(center_x, center_y, yellow_x, yellow_y):
    # Movement directions:
    # 0 -> stop
    # 1 -> up
    # 2 -> down
    # 3 -> left
    # 4 -> right
    tol = 50  # Tolerance for considering the target reached

    # Calculate the differences in x and y coordinates
    dx = int(yellow_x) - int(center_x)
    dy = int(yellow_y) - int(center_y)

    # If yellow item not found
    if int(yellow_x) == 0 or int(yellow_y) == 0:
        send_msg("0")
    else:
        # Check whether to move up, down, left, or right
        if both x and y coordinate in the tolerance range/target is reached:
            # Stop
        else:
            # Only move vertically (y-axis) if x attained
                if dy < 0
                    # Move backward
                else:
                    # Move frontward
            # Only move horizontally (x-axis) if y attained
                if dx < 0:
                    # Move left
                else:
                    # Move right
            # Move both horizontally and vertically at the same time
            else:
                if dx < 0:
                    if dy < 0:
                        # Move back and left
                    else:
                        # Move up and left
                else:
                    if dy < 0:
                        # Move back and right
                    else:
                        # Move up and right

```
[1]:https://codeantenna.com/a/2OhcDHzc2B 


