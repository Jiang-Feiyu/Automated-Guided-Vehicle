import serial

ser = serial.Serial('/dev/ttyUSB0', 9600) # 串口设备和波特率要和Arduino一致

while True:
    data = ser.readline().decode('utf-8').strip()
    print(f"Received data: {data}")
