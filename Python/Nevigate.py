import cv2
import numpy as np
import time
import serial
import serial.tools.list_ports

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

def detect_and_draw_largest_red_object(frame, prev_center_x, prev_center_y):
    # Your existing code for object detection and tracking

def navigate_to_origin(prev_center_x, prev_center_y, tolerance):
    # Your logic for navigating towards the origin

def get_move_command(dx, dy, tolerance):
    # Your logic for determining the move command based on dx, dy, and tolerance
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
