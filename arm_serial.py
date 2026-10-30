
import time
import serial


class ArmSerialController:
    def __init__(self, port="COM7", baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(
                self.port,
                self.baud_rate,
                timeout=1
            )
            time.sleep(2)
            self.ser.reset_input_buffer()
            print(f"Connected to ESP32 on {self.port}")
            return True

        except serial.SerialException as error:
            print(f"ESP32 connection failed: {error}")
            return False

    def send_command(self, command):
        if self.ser is None or not self.ser.is_open:
            print("ERROR: ESP32 is not connected")
            return False

        if command not in ("PICK_RED", "PICK_BLUE", "HOME"):
            print("ERROR: Invalid arm command")
            return False

        try:
            self.ser.write((command + "\n").encode("utf-8"))
            self.ser.flush()

            deadline = time.time() + 90
            acknowledged = False

            while time.time() < deadline:
                reply = self.ser.readline().decode(
                    "utf-8", errors="replace"
                ).strip()

                if not reply:
                    continue

                print("ESP32:", reply)

                if reply.startswith("ERROR:"):
                    return False

                if reply == "ACK:START_PICK":
                    acknowledged = True

                if reply == "DONE":
                    return acknowledged or command == "HOME"

            print("ERROR: Timed out waiting for ESP32")
            return False

        except (serial.SerialException, OSError) as error:
            print(f"Serial communication error: {error}")
            return False

    def close(self):
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
            print("ESP32 serial connection closed")
