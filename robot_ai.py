
import cv2
import numpy as np
import serial
import time

# ---------------- CONNECTION SETTINGS ----------------
CAMERA_URL = "http://10.123.175.11:8080/video"
SERIAL_PORT = "COM7"
BAUD_RATE = 115200

# ---------------- RED DEBRIS DETECTION ----------------
RED_LOW_1 = np.array([0, 100, 60])
RED_HIGH_1 = np.array([10, 255, 255])

RED_LOW_2 = np.array([170, 100, 60])
RED_HIGH_2 = np.array([179, 255, 255])

MINIMUM_AREA = 500
STABLE_FRAMES_REQUIRED = 8
CLEAR_SECONDS_TO_REARM = 2.0

def find_red_debris(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, RED_LOW_1, RED_HIGH_1)
    mask2 = cv2.inRange(hsv, RED_LOW_2, RED_HIGH_2)
    mask = cv2.bitwise_or(mask1, mask2)

    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    valid = [
        c for c in contours
        if cv2.contourArea(c) >= MINIMUM_AREA
    ]

    if not valid:
        return None

    return max(valid, key=cv2.contourArea)


def main():
    esp = None
    camera = None

    stable_frames = 0
    red_triggered = False
    red_absent_since = None

    try:
        print(f"Connecting to ESP32 on {SERIAL_PORT}...")

        esp = serial.Serial(
            SERIAL_PORT, BAUD_RATE, timeout=0.1
        )

        # Opening the serial port may reset the ESP32.
        time.sleep(2)
        esp.reset_input_buffer()

        print("Connecting to phone camera...")
        camera = cv2.VideoCapture(CAMERA_URL)

        if not camera.isOpened():
            raise RuntimeError(
                "Camera unavailable. Check the phone IP, "
                "Wi-Fi, IP Webcam app and /video URL."
            )

        print("RED DEBRIS AUTO-DETECTION ACTIVE")
        print("Stable red detection will send PICK_RED once.")
        print("Press Q in the camera window to quit.")

        while True:
            ok, frame = camera.read()

            if not ok:
                stable_frames = 0
                print("Camera frame unavailable.")
                time.sleep(0.1)
                continue

            contour = find_red_debris(frame)
            now = time.monotonic()

            if contour is not None:
                x, y, w, h = cv2.boundingRect(contour)

                cv2.rectangle(
                    frame, (x, y), (x + w, y + h),
                    (0, 0, 255), 2
                )
                cv2.putText(
                    frame, "RED DEBRIS DETECTED",
                    (x, max(25, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 2
                )

                stable_frames += 1
                red_absent_since = None

                if (
                    stable_frames >= STABLE_FRAMES_REQUIRED
                    and not red_triggered
                ):
                    print("Red debris confirmed!")
                    print("Sending PICK_RED to COM7...")

                    esp.write(b"PICK_RED\n")
                    esp.flush()

                    red_triggered = True
                    print("PICK_RED sent. Waiting for red to clear.")

            else:
                stable_frames = 0

                if red_absent_since is None:
                    red_absent_since = now

                elif (
                    red_triggered
                    and now - red_absent_since >= CLEAR_SECONDS_TO_REARM
                ):
                    red_triggered = False
                    print("Red area clear. Ready for next object.")

            if red_triggered:
                status = "PICK SENT - waiting for red to clear"
            else:
                status = "Searching for red debris"

            cv2.putText(
                frame, status, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 255, 0), 2
            )

            cv2.imshow("Robot AI - Red Debris Detection", frame)

            # Display ESP32 messages, including ACK and DONE.
            while esp.in_waiting:
                line = esp.readline().decode(
                    "utf-8", errors="replace"
                ).strip()
                if line:
                    print("ESP32:", line)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except serial.SerialException as exc:
        print("Serial error:", exc)
        print("Check COM7 and close Arduino Serial Monitor.")

    except Exception as exc:
        print("Error:", exc)

    finally:
        if camera is not None:
            camera.release()

        cv2.destroyAllWindows()

        if esp is not None and esp.is_open:
            esp.close()

        print("Robot AI stopped.")


if __name__ == "__main__":
    main()
