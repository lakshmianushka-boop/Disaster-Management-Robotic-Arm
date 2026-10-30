# Vision-Assisted Robotic Debris Collection Using a Mobile Robot and Servo Arm


This project presents a low-cost mobile robotic platform that combines wireless vehicle control, computer vision, and a servo-based robotic arm to detect and collect objects based on their colour.

The system uses an ESP32-controlled mobile robot, an ESP32-based robotic arm with a PCA9685 servo driver, and a laptop-based computer vision application developed using Python and OpenCV.

The robot is manually navigated to the target area. A smartphone camera provides a live video stream to the laptop, where the vision system identifies red-coloured objects. Once a red object is detected consistently across multiple frames, the Python application sends a command to the robotic arm through USB serial communication. The arm then performs a predefined pick-and-place sequence.

## System Architecture

The project consists of three main modules:

1. **Mobile Robot:** Controlled wirelessly using an ESP32-hosted Wi-Fi webpage and an L298N motor driver.
2. **Computer Vision System:** Uses a smartphone camera, Python, and OpenCV to detect red-coloured objects.
3. **Robotic Arm:** Uses an ESP32, PCA9685 servo driver, and four SG90 servo motors to perform pick-and-place operations.

### Workflow

1. The user connects to the robot's Wi-Fi network.
2. The mobile robot is manually driven towards the target area.
3. A smartphone camera streams live video to the laptop.
4. The Python application processes the video and detects red-coloured objects.
5. After stable detection, the application sends the `PICK_RED` command through USB serial communication.
6. The robotic arm executes its programmed pick-and-place sequence.
7. The arm releases the object at its predefined drop location and returns to its home position.

## Hardware Requirements

| Component | Purpose |
|---|---|
| ESP32 development boards | Robot and arm controllers |
| L298N motor driver | Controls the DC motors |
| DC geared motors | Mobile robot movement |
| Robot chassis and wheels | Mobile platform |
| PCA9685 16-channel servo driver | Controls arm servos |
| 4 × SG90 servo motors | Arm movement and gripping |
| Battery supply | Powers the mobile robot |
| Regulated 5V supply | Powers the servo motors |
| Smartphone camera | Provides live video |
| Laptop or PC | Runs the computer vision application |

## Software Requirements

- Arduino IDE
- Python 3
- OpenCV
- NumPy
- PySerial
- ESP32 Arduino board support package
- Adafruit PWM Servo Driver Library

## Repository Structure

```text
Vision-Assisted-Mobile-Robot/
│
├── car_control/
│   └── car_control.ino
│
├── robotic_arm/
│   └── robotic_arm.ino
│
├── vision_system/
│   └── robot_ai.py
│
├── requirements.txt
└── README.md
```

*The folder and file names above are illustrative. Adjust them to match the actual names in this repository.*

## Module 1: Mobile Robot Control

The mobile robot uses an ESP32 microcontroller connected to an L298N motor driver.

The ESP32 creates a Wi-Fi access point and hosts a simple web-based control interface. A phone or laptop connected to this network can control the robot using directional buttons.

### Motor Driver Connections

| L298N Pin | ESP32 GPIO |
|---|---|
| IN1 | GPIO 26 |
| IN2 | GPIO 25 |
| IN3 | GPIO 33 |
| IN4 | GPIO 32 |
| ENA | Jumper installed |
| ENB | Jumper installed |

The motor battery is connected to the L298N motor supply terminals. The motors are connected to the driver output terminals.

### Control Commands

| Command | Function |
|---|---|
| F | Forward |
| B | Backward |
| L | Left |
| R | Right |
| S | Stop |

The mobile robot is manually operated and positioned near the target object.

## Module 2: Computer Vision and Object Detection

The computer vision module is developed using Python and OpenCV.

A smartphone camera provides a live video stream to the laptop. The application processes the incoming frames and identifies red-coloured objects using HSV colour segmentation.

### Detection Process

1. Capture a frame from the smartphone camera stream.
2. Convert the frame from BGR colour space to HSV.
3. Apply red-colour thresholding.
4. Combine the red masks to identify red pixels across the HSV hue range.
5. Apply contour detection.
6. Filter detected contours based on minimum area.
7. Check whether the detection remains stable across consecutive frames.
8. Send the `PICK_RED` command when the detection condition is satisfied.

### Detection Parameters

| Parameter | Configuration |
|---|---|
| Colour detection | Red |
| Colour space | HSV |
| Minimum contour area | 500 pixels |
| Stable detection threshold | 8 frames |
| Serial communication speed | 115200 baud |
| Communication protocol | USB Serial |

The current implementation uses traditional colour-based computer vision rather than a trained deep-learning model.

## Module 3: Robotic Arm and Pick-and-Place

The robotic arm is controlled by an ESP32 connected to a PCA9685 servo driver.

Four SG90 servo motors control the base, shoulder, elbow, and gripper.

### PCA9685 Connections

| PCA9685 Pin / Channel | Connection |
|---|---|
| VCC | ESP32 3.3V |
| GND | Common GND |
| SDA | ESP32 GPIO 21 |
| SCL | ESP32 GPIO 22 |
| V+ | External regulated 5V servo supply |
| Channel 4 | Base servo |
| Channel 5 | Shoulder servo |
| Channel 6 | Elbow servo |
| Channel 7 | Gripper servo |

### Arm Commands

| Command | Function |
|---|---|
| `PICK_RED` | Executes the configured red-object pick-and-place sequence |
| `PICK_BLUE` | Executes the configured alternate pick-and-place sequence |
| `HOME` | Returns the arm to its home position |

The arm receives commands through USB serial communication at 115200 baud.

The pick-and-place movement is based on predefined servo angles and a programmed sequence. The current implementation does not use inverse kinematics or real-time object-coordinate mapping.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL with the actual GitHub repository URL.

### 2. Install Python Dependencies

Make sure Python 3 is installed.

```bash
pip install -r requirements.txt
```

If a requirements file has not been created, use:

```bash
pip install opencv-python numpy pyserial
```

### 3. Upload the Mobile Robot Firmware

1. Open the car control `.ino` file in Arduino IDE.
2. Select the correct ESP32 board and COM port.
3. Upload the firmware.
4. Connect a phone or laptop to the ESP32 Wi-Fi network.
5. Open the IP address displayed in the Serial Monitor to access the control webpage.

### 4. Upload the Robotic Arm Firmware

1. Connect the arm ESP32 to the computer.
2. Open the robotic arm `.ino` file in Arduino IDE.
3. Select the correct ESP32 board and COM port.
4. Upload the firmware.
5. Ensure the PCA9685 and external servo power connections are correct.

### 5. Configure and Run the Vision System

Before running the Python application, configure:

- Smartphone camera stream URL.
- Correct serial COM port for the arm ESP32.
- Serial baud rate of 115200.

Then run:

```bash
python robot_ai.py
```

Close the Arduino Serial Monitor before running the Python program if both applications need to access the same COM port.

## Safety Considerations

- Use a regulated external 5V supply for the servo motors.
- Connect the grounds of the ESP32, PCA9685, and servo supply together.
- Never connect 5V directly to the ESP32 3.3V pin.
- Verify the servo movement range and mechanical limits before operating the arm.
- Keep the robot wheels lifted during initial motor tests.
- Keep the motor and servo power supplies properly rated for their loads.
- Stop testing if any servo continuously buzzes, overheats, or strains.
- Keep an accessible power switch for emergency shutdown.

## Current Implementation and Limitations

The project demonstrates the integration of wireless mobile robot control, colour-based computer vision, serial command communication, and robotic pick-and-place control.

The current implementation has the following limitations:

- The mobile robot is manually navigated rather than autonomously driven.
- Red-object detection is based on HSV colour thresholding and contour filtering.
- The vision system does not calculate calibrated 3D object coordinates.
- The robotic arm uses predefined servo angles and movement sequences.
- The system does not currently implement inverse kinematics or closed-loop object-position correction.
- Successful end-to-end object collection depends on mechanical alignment, servo calibration, lighting conditions, and reliable motor operation.

## Future Enhancements

- Add autonomous obstacle detection and navigation.
- Implement object-position estimation and camera-to-arm calibration.
- Introduce more robust object classification.
- Add feedback sensors for improved arm positioning.
- Integrate mobile robot and robotic arm control into a unified communication system.
- Improve reliability through real-time monitoring and safety mechanisms.

## Project Objective

The main objective is to develop an affordable vision-assisted mobile robotic platform capable of identifying coloured objects and performing programmed pick-and-place operations.

The project demonstrates the practical application of embedded systems, wireless communication, computer vision, and robotic manipulation.

## Technologies Used

- **Microcontroller:** ESP32
- **Motor Driver:** L298N
- **Servo Driver:** PCA9685
- **Actuators:** SG90 servo motors and DC geared motors
- **Programming Languages:** C++ and Python
- **Computer Vision:** OpenCV
- **Communication:** Wi-Fi and USB Serial

## Authors

LAKSHMI ANUSHKA PERURI - 24BRS1320
KOLLI JUHITHASARI - 24BRS1320

## License

This project is developed for academic and educational purposes. Add a suitable open-source license if you intend to permit reuse and redistribution.
