import cv2
import numpy as np
import time
import serial
import serial.tools.list_ports
cap = cv2.VideoCapture(0)

def find_arduino_port():
    ports = serial.tools.list_ports.grep("1a86:7523")
    for port, desc, hwid in ports:
        return port
    return None

def init_serial_connection():
    arduino_port = find_arduino_port()
    print("arduino_port:", arduino_port)

    if arduino_port:
        try:
            ser = serial.Serial(arduino_port, 9600, timeout=1)
            print("Serial name:", ser.name)
            print("Serial baudrate:", ser.baudrate)
            print("Serial state:", ser.is_open)
            return ser
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            return None
    else:
        print("Arduino not found.")
        return None
        

       
       
        
prev_center_x = None
prev_center_y = None

# Lists to store the movement history
movement_history = []
        
def detect_and_draw_largest_red_object(frame, prev_center_x, prev_center_y):
    # Your existing code for object detection and tracking
  global prev_center_x, prev_center_y
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

        # Print movement direction based on changes in coordinates
        if prev_center_x is not None and prev_center_y is not None:
            dx = center_x - prev_center_x
            dy = center_y - prev_center_y

          if dx < 0 
            horizontal_movement = "left" 
            print("Moving left")
          else 
            horizontal_movement = "right"
            print("Moving right")
          if dy < 0 
            vertical_movement = "down"
             print("Moving down")
          else "down"
            vertical_movement = "up" 
             print("Moving up")

            movement = f"Movement: {horizontal_movement} {vertical_movement}"
            movement_history.append(movement)
            print(movement)

        # Update previous center coordinates
        prev_center_x = center_x
        prev_center_y = center_y

    cv2.imshow('Largest Red Object Detection', frame)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    detect_and_draw_largest_red_object(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Add a delay of 0.5 seconds
    time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()

    
    
    
def navigate_to_origin(prev_center_x, prev_center_y, tolerance):
    # Your logic for navigating towards the origin
  coordinates and the origin (0, 0)
    dx = 0 - prev_center_x
    dy = 0 - prev_center_y

    # Move the car based on the difference in x and y coordinates
    move_command = get_move_command(dx, dy, tolerance)
    ser.write(f"{move_command}\r\n".encode('utf-8'))

    # Wait for the car to reach the origin
    time.sleep(5)

    # Stop the car
    stop_command = get_stop_command()
    ser.write(f"{stop_command}\r\n".encode('utf-8'))
    
    
    

def get_move_command(dx, dy, tolerance):
    # Your logic for determining the move command based on dx, dy, and tolerance
    if abs(dx) < tolerance and abs(dy) < tolerance:
        return "STOP"
    elif abs(dx) >= tolerance and abs(dy) < tolerance:
        if dx > 0:
            return "MOVE_RIGHT"
        else:
            return "MOVE_LEFT"
    elif abs(dx) < tolerance and abs(dy) >= tolerance:
        if dy > 0:
            return "MOVE_DOWN"
        else:
            return "MOVE_UP"
    else:
        if dx > 0 and dy > 0:
            return "MOVE_DOWN_RIGHT"
        elif dx > 0 and dy < 0:
            return "MOVE_UP_RIGHT"
        elif dx < 0 and dy > 0:
            return "MOVE_DOWN_LEFT"
        else:
            return "MOVE_UP_LEFT"
    return move_command

    


    
def main():
    ser = init_serial_connection()

    if ser is None:
        print("Serial connection failed. Exiting.")
        return

    cap = cv2.VideoCapture(0)

    prev_center_x = None
    prev_center_y = None
    tolerance = 200

    try:
        while 1:
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture frame. Exiting...")
                break

            detect_and_draw_largest_red_object(frame, prev_center_x, prev_center_y)

            move_command = get_move_command(prev_center_x, prev_center_y, tolerance)
            print("Move command sent:", move_command)
            ser.write(f"{move_command}\r\n".encode('utf-8'))

            response = ser.readline().decode('utf-8').strip()
            print("res:", response)

            time.sleep(5)

    except KeyboardInterrupt:
        print("KeyboardInterrupt. Exiting.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        ser.close()

if __name__ == "__main__":
    main()
