AQUA-RESQ Gazebo Simulation
This directory documents the Gazebo simulation setup used for the AQUA-RESQ software proof-of-concept.

Simulation Environment
The simulation was developed using:

Ubuntu 24.04
ROS 2 Jazzy
Gazebo Harmonic
PX4 SITL
Micro XRCE-DDS
PX4 ROS 2 messages
Simulated UAV
The simulation uses a PX4-compatible quadrotor model in Gazebo.

An RGB camera was added to the simulated UAV and connected to the ROS 2 perception pipeline.

The camera publishes:

/aqua_resq/camera/image
The camera feed is bridged from Gazebo to ROS 2 using ros_gz_bridge.

Camera Pipeline
Gazebo UAV
     ↓
Simulated RGB Camera
     ↓
Gazebo Camera Topic
     ↓
ros_gz_bridge
     ↓
ROS 2 Image Topic
     ↓
CvBridge
     ↓
OpenCV
     ↓
YOLOv8
PX4 Position Pipeline

The simulated UAV publishes global-position information through PX4.

The relevant ROS 2 topic is:

/fmu/out/vehicle_global_position

The camera_viewer.py node subscribes to this topic and associates the UAV position with detected people.

AI Perception Pipeline

The perception node performs the following steps:

Receive camera frames from ROS 2.
Convert the ROS 2 image using CvBridge.
Run YOLOv8 inference.
Identify person detections.
Obtain the latest valid UAV position from PX4.
Associate the detection with the UAV location.
Save the latest detection as JSON.
Display the annotated camera feed.
Detection Output

The detection node writes:

~/aqua_gazebo_test/latest_detections.json

The JSON is consumed by the AQUA-RESQ Streamlit dashboard.

ROS 2 to Dashboard Flow
PX4 SITL
   ↓
Vehicle Global Position
   ↓
ROS 2
   ↓
camera_viewer.py
   ↓
YOLOv8
   ↓
latest_detections.json
   ↓
Streamlit Dashboard
Notes

The Gazebo environment is used for software development and demonstration.

The simulated UAV, camera, GPS position, and detected targets do not represent measurements from a physical aircraft.

Physical deployment would require hardware integration, flight testing, sensor calibration, communication validation, and appropriate safety procedures
