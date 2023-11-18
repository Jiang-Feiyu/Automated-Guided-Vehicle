import serial
import time

def connect_arduino(port, baudrate):
    try:
        # 打开串口
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"成功连接到Arduino，端口：{ser.name}, 波特率：{baudrate}")
        return ser
    except serial.SerialException as e:
        print(f"连接失败：{e}")
        return None

def send_command(ser, command):
    try:
        # 发送指令
        ser.write(command.encode())
        print(f"已发送指令: {command}")
    except serial.SerialException as e:
        print(f"发送指令失败：{e}")

def main():
    # 请替换成你的软串口端口和波特率
    arduino_port = "/dev/rfcomm0"  # 根据实际情况修改
    baud_rate = 9600  # 根据实际情况修改

    # 连接到Arduino
    arduino_serial = connect_arduino(arduino_port, baud_rate)

    if arduino_serial is not None:
        try:
            while True:
                # 向Arduino发送指令
                send_command(arduino_serial, "This is python")

                # 可以添加其他操作或者休眠一段时间
                time.sleep(1)  # 休眠1秒

        except KeyboardInterrupt:
            # 如果用户按下Ctrl+C，停止发送指令
            pass
        finally:
            # 关闭串口连接
            arduino_serial.close()
            print("已关闭串口连接")

if __name__ == "__main__":
    main()
