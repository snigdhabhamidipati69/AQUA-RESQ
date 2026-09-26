# AQUA-RESQ Gazebo Simulation

This directory documents the Gazebo simulation setup used for the AQUA-RESQ software proof-of-concept.

## Simulation Environment

The simulation was developed using:

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- PX4 SITL
- Micro XRCE-DDS
- PX4 ROS 2 messages

## Simulated UAV

The simulation uses a PX4-compatible quadrotor model in Gazebo.

An RGB camera was added to the simulated UAV and connected to the ROS 2 perception pipeline.

The camera publishes:

```text
/aqua_resq/camera/image

The camera feed is bridged from Gazebo to ROS 2 using ros_gz_bridge.

Camera Pipeline

The simulated camera provides RGB images to the ROS 2 perception node.

The perception pipeline consists of:

Gazebo simulated RGB camera
ros_gz_bridge
ROS 2 image topic
CvBridge
OpenCV
YOLOv8

The YOLOv8 model processes the camera frames and identifies person detections.

PX4 Position Pipeline

The simulated UAV publishes global-position information through PX4.

The relevant ROS 2 topic is:

/fmu/out/vehicle_global_position

The camera_viewer.py node subscribes to this topic and associates the UAV position with detected people.

The position data includes:

Latitude
Longitude
Altitude
AI Perception

The perception node performs the following operations:

Receives camera frames from ROS 2.
Converts the ROS 2 image using CvBridge.
Runs YOLOv8 inference.
Identifies person detections.
Obtains the latest valid UAV position from PX4.
Associates the detection with the UAV location.
Saves the latest detection as JSON.
Displays the annotated camera feed.
Detection Output

The detection node writes the latest detection to:

~/aqua_gazebo_test/latest_detections.json

The JSON output is used by the AQUA-RESQ Streamlit dashboard to display the detected target and its associated location.

ROS 2 and Dashboard Integration

The Gazebo simulation provides the camera and UAV position data used by the ROS 2 perception pipeline.

The perception node combines the camera detection and simulated UAV position before writing the detection information to the JSON file.

The Streamlit dashboard reads the JSON data and displays the latest detection information.

Simulation Notes

The Gazebo environment is used for software development, integration, testing, and demonstration.

The simulated UAV, camera, GPS position, and detected targets do not represent measurements from a physical aircraft.

The current simulation demonstrates the software perception and dashboard pipeline. Physical deployment would require hardware integration, sensor calibration, communication validation, autonomous navigation testing, safety mechanisms, and field trials.
