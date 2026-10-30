
import time
import serial


class ArmLink:
    def __init__(self, port, baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(
                self.port,
                self.baud_rate,
                timeout=3
            )
            time.sleep(2)
            self.connection.reset_input_buffer()
            print(f"Connected to ESP32 on {self.port}")
            return True

        except serial.SerialException as error:
            print(f"ESP32 connection failed: {error}")
            self.connection = None
            return False

    def send_command(self, command):
        if self.connection is None or not self.connection.is_open:
            print("ESP32 is not connected.")
            return False

        try:
            self.connection.write((command + "\n").encode())
            self.connection.flush()

            reply = self.connection.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            print(f"ESP32 reply: {reply}")

            return reply == "DONE"

        except serial.SerialException as error:
            print(f"Communication error: {error}")
            return False

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("ESP32 connection closed.")

