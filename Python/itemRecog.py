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

def detect_and_draw_largest_red_object(frame):
    prev_center_x = 0
    prev_center_y = 0

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
        prev_center_x = x + w // 2
        prev_center_y = frame.shape[0] - (y + h // 2)  # Invert y coordinate

        print("Red coordinates:", prev_center_x, prev_center_y)

    cv2.imshow('Largest Red Object Detection', frame)

    return prev_center_x, prev_center_y

def detect_and_record_largest_yellow_object(frame):
    prev_yellow_x = 0
    prev_yellow_y = 0

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
        prev_yellow_x = x + w // 2
        prev_yellow_y = frame.shape[0] - (y + h // 2)  # Invert y coordinate

        print("Yellow coordinates:", prev_yellow_x, prev_yellow_y)

    cv2.imshow('Largest Yellow Object Detection', frame)

    return prev_yellow_x, prev_yellow_y


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

        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        center_x, center_y = detect_and_draw_largest_red_object(frame)
        yellow_x, yellow_y = detect_and_record_largest_yellow_object(frame)
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
