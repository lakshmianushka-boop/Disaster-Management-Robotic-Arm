# Disaster-Management-Robotic-Arm
Vision-Guided AI-Based Robotic Arm for Autonomous Debris Detection and Obstacle Removal in Disaster Management

# Project Overview

Natural disasters and structural collapses often expose rescue personnel to hazardous environments while locating and assisting trapped victims. This project proposes an **AI Vision-Based Search and Rescue Robotic Arm** that combines computer vision with a robotic manipulator to assist in search and rescue operations.

The system aims to detect human victims using an AI-based vision model and guide a robotic arm to interact with lightweight emergency objects or perform safe assistance tasks. By reducing direct human intervention in dangerous environments, the proposed system seeks to improve rescue efficiency and responder safety.

---

# Problem Statement

Develop an AI-powered robotic arm capable of detecting human victims in simulated search-and-rescue environments using computer vision and performing accurate object manipulation. The system should process camera images, identify the target location, estimate its position, and control a multi-degree-of-freedom robotic arm to execute the required movement with improved accuracy and reliability.

---

# Objectives

- Detect human victims using computer vision.
- Estimate target location from image data.
- Control a robotic arm for object manipulation.
- Integrate AI vision with robotic control.
- Develop a low-cost prototype for educational and research purposes.

---

# Proposed System Architecture

The proposed system consists of the following stages:

1. Image Acquisition
2. Image Preprocessing
3. AI-Based Human Detection
4. Target Localization
5. Inverse Kinematics Computation
6. Servo Motor Control
7. Robotic Arm Movement
8. Output and Performance Evaluation

---

# Technologies Used

## Hardware

- 4-DOF Robotic Arm
- MG90 Servo Motors
- Arduino Uno
- PCA9685 Servo Driver
- USB Camera
- External Power Supply

## Software

- Python
- Arduino IDE
- OpenCV
- YOLO
- NumPy
