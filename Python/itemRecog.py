import cv2
import numpy as np
import time
import requests
import serial
import serial.tools.list_ports
import time

# Variables to track the previous center coordinates
prev_center_x = None
prev_center_y = None
prev_yellow_x = None
prev_yellow_y = None

def detect_object(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Define the range of yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the HSV image to get only red colors
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # Threshold the HSV image to get only yellow colors
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Find contours in the red mask
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find contours in the yellow mask
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to keep track of the largest contours and their areas
    largest_red_contour = None
    largest_yellow_contour = None
    largest_red_area = 0
    largest_yellow_area = 0

    # Process red contours
    for contour in red_contours:
        area = cv2.contourArea(contour)
        if area > 100:
            if area > largest_red_area:
                largest_red_area = area
                largest_red_contour = contour

    # Process yellow contours
    for contour in yellow_contours:
        area = cv2.contourArea(contour)
        if area > 100:
            if area > largest_yellow_area:
                largest_yellow_area = area
                largest_yellow_contour = contour

    # Draw rectangle around the largest red object
    if largest_red_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_red_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the center of the rectangle
        red_center_x = x + w // 2
        red_center_y = frame.shape[0] - (y + h // 2)  # Invert y coordinate

        print("Red coordinates:", red_center_x, red_center_y)
    else:
        red_center_x, red_center_y = 0, 0

    # Draw rectangle around the largest yellow object
    if largest_yellow_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_yellow_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        # Calculate the center of the rectangle
        yellow_center_x = x + w // 2
        yellow_center_y = frame.shape[0] - (y + h // 2)  # Invert y coordinate

        print("Yellow coordinates:", yellow_center_x, yellow_center_y)
    else:
        yellow_center_x, yellow_center_y = 0, 0

    cv2.imshow('Object Detection', frame)

    return red_center_x, red_center_y, yellow_center_x, yellow_center_y

# 向server发送http请求
def http_send(server_address, message):
    try:
        # 发送HTTP POST请求，将消息发送给服务器
        response_post = requests.post(server_address, data={'message': message})

        # Check if the request was successful (status code 200)
        if response_post.status_code == 200:
            print("Server Response:")
            print(response_post.text)
        else:
            print(f"Error: Server returned status code {response_post.status_code}")
    except Exception as e:
        print(f"Error during HTTP request: {e}")


def main():
    cap = cv2.VideoCapture(0)
    server_address = 'http://192.168.50.183:8888'

    while cap.isOpened():
        ret, frame = cap.read()

        # 获取摄像头的帧宽度和帧高度
        # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print(frame_width)
        # print(frame_height)

        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        center_x, center_y, yellow_x, yellow_y = detect_object(frame)
        msg=str(center_x)+" "+str(center_y)+" "+str(yellow_x)+" "+str(yellow_y)
        print("msg------->", msg)
        http_send(server_address,msg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Add a delay of 0.5 seconds
        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()

main()
