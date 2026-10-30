
import time


class ArmSimulator:
    """Software-only stand-in for the ESP32 arm."""

    def __init__(self):
        self.connected = False
        self.busy = False
        self.completed_cycles = 0

    def connect(self):
        self.connected = True
        print("[SIM] ESP32 connected (simulated).")
        return True

    def send_command(self, command):
        if not self.connected:
            print("[SIM] ERROR: Arm is not connected.")
            return False

        if self.busy:
            print("[SIM] ERROR: Arm is already busy.")
            return False

        if command not in ("PICK_RED", "PICK_BLUE"):
            print(f"[SIM] ERROR: Unknown command: {command}")
            return False

        self.busy = True
        print(f"[SIM] Received: {command}")
        print("[SIM] Performing one simulated pick-and-drop cycle...")

        try:
            time.sleep(1)
            self.completed_cycles += 1
            print("[SIM] ESP32 reply: DONE")
            return True
        finally:
            self.busy = False

    def close(self):
        self.connected = False
        print("[SIM] Disconnected.")
