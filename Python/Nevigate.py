import serial
import serial.tools.list_ports
import time
import cv2
import numpy as np
# Variables to track the previous center coordinates
prev_center_x = 0
prev_center_y = 0
tol = 40
finished = 0
cap = cv2.VideoCapture(0)

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
        
# 返回当前坐标
def loc(frame):
    global prev_center_x, prev_center_y

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to keep track of the largest contour and its area
    largest_contour = None
    largest_area = 0

    for contour in contours:
        # Calculate area to filter out small contours (noise)
        area = cv2.contourArea(contour)
        if area > 100:
            # Update largest contour if current contour has a larger area
            if area > largest_area:
                largest_area = area
                largest_contour = contour

    if largest_contour is not None:
        # Draw rectangle around the largest red object
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the center of the rectangle
        center_x = x + w // 2
        center_y = frame.shape[0] - (y + h // 2)  # Invert y coordinate

        print("Center coordinates:", center_x, center_y)

        # Update previous center coordinates
        prev_center_x = center_x
        prev_center_y = center_y

    cv2.imshow('Largest Red Object Detection', frame)

# 检查是否完成
def chk_finished(x,y):
    global prev_center_x, prev_center_y, finished
    # Calculate the differences in x and y coordinates
    dx = x - prev_center_x
    dy = y - prev_center_y
    
    if abs(dx) <= tol and abs(dy) <= tol:
        time.sleep(1)
        if abs(dx) <= tol and abs(dy) <= tol:
            return True
    return False
    
# 打开图像
def img(x, y):
    global finished
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        loc(frame)
        navigate_to_point(x,y)
        
        if chk_finished(x,y) == 1:
            finished
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Add a delay of 0.5 seconds
        time.sleep(0.5)

# 用户选择行车模式
def mode():
    while True:
        print("Please choose your function:")
        print("0: Back to the origin point   1: Go to specific coordinate   2: exit")
        response = input()
        
        if response.startswith("0"):
            # 用户输入以"0"开头，小车移动到摄像头识别的位置的中心点(x, y)
            print(response)
            return (0,0,0) 
        elif response.startswith("1"):
            # 用户输入以"1"开头，需要提供坐标(x, y)
            print(response)
            try:
                coordinates = input("Please enter the coordinates (x, y): ")
                x, y = map(int, coordinates.strip('()').split(','))
                return (1, x, y)
            except ValueError:
                print("Invalid coordinates format. Please enter coordinates in the format (x, y).")
        elif response.startswith("2"):
            return (2,0,0)
        else:
            print("Invalid choice. Please choose 0 or 1.")

# 导航程序
def navigate_to_point(x,y):
    # 请你帮我完善navigate函数，通过send_msg("("+str(i)+")")的方式控制小车的前后左右移动
    # 移动方向： 0 -> stop 
    # 1 -> up 
    # 2 -> down 
    # 3 -> left 
    # 4 -> right 
    global prev_center_x, prev_center_y, tol

    # Calculate the differences in x and y coordinates
    dx = x - prev_center_x
    dy = y - prev_center_y

    # Check whether to move up, down, left, or right
    if abs(dx) <= tol and abs(dy) <= tol:
        # Stop if the target is reached
        send_msg("(0)")
    elif abs(dx) > abs(dy):
        # Move left or right
        if dx > 0:
            # Move right
            send_msg("(4)")
        else:
            # Move left
            send_msg("(3)")
    else:
        # Move up or down
        if dy > 0:
            # Move down
            send_msg("(2)")
        else:
            # Move up
            send_msg("(1)")

    
def main():
    global finished
    while True:
        choice, x, y = mode()
        
        # Process the return values from mode() as needed
        if choice == 0:
            # Handle the case when the user chose to go back to the origin
            print("Returning to the origin point.")
            while (finished == 0):
                img(0,0)
            finished = 0
            print("Task finished")
        elif choice == 1:
            # Handle the case when the user chose to go to a specific coordinate
            print(f"Going to specific coordinate: ({x}, {y})")
            while (finished == 0):
                img(x,y)
            finished = 0
            print("Task finished")
        elif choice == 2:
            # Handle the case when the user chose to go to a specific coordinate
            print("Exit!")
            break
        else:
            # This should not be reached, but handle it if needed
            print("Invalid choice.")

main()
