import cv2
import numpy as np
import time

import requests
import serial
import serial.tools.list_ports
import time


cap = cv2.VideoCapture(0)
server_address = 'http://192.168.50.69:8888'

# Variables to track the previous center coordinates
prev_center_x = None
prev_center_y = None
prev_yellow_x = None
prev_yellow_y = None

# Lists to store the movement history
movement_history = []

def detect_and_draw_largest_red_object(frame):
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

        print("Red coordinates:", center_x, center_y)

        # Print movement direction based on changes in coordinates
        if prev_center_x is not None and prev_center_y is not None:
            dx = center_x - prev_center_x
            dy = center_y - prev_center_y

            horizontal_movement = "left" if dx < 0 else "right"
            vertical_movement = "up" if dy < 0 else "down"

            movement = f"Movement: {horizontal_movement} {vertical_movement}"
            movement_history.append(movement)
            print(movement)

        # Update previous center coordinates
        prev_center_x = center_x
        prev_center_y = center_y

    cv2.imshow('Largest Red Object Detection', frame)

def detect_and_record_largest_yellow_object(frame):
    global prev_yellow_x, prev_yellow_y

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

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
        # Draw rectangle around the largest yellow object
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        # Calculate the center of the rectangle
        center_x = x + w // 2
        center_y = frame.shape[0] - (y + h // 2)  # Invert y coordinate

        print("Yellow coordinates:", center_x, center_y)

        # Update previous yellow object coordinates
        prev_yellow_x = center_x
        prev_yellow_y = center_y

    cv2.imshow('Largest Yellow Object Detection', frame)


# 向server发送http请求
def http_send(server_address, message):
    # 发送HTTP POST请求，将消息发送给服务器
    response_post = requests.post(server_address, data=message)

    # 打印服务器的响应
    print("Server Response:")
    print(response_post.text)

# 监听轮询
def listen_to_server(server_address):
    # 发送用户输入的消息给服务器
    http_send(server_address, prev_center_x)
    http_send(server_address, prev_center_y)
    http_send(server_address, prev_yellow_x)
    http_send(server_address, prev_yellow_y)



while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    detect_and_draw_largest_red_object(frame)
    detect_and_record_largest_yellow_object(frame)
    listen_to_server(server_address)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Add a delay of 0.5 seconds
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()


