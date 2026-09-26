# AQUA-RESQ

## From Sky to Subsurface: One Mission, Two Worlds

AQUA-RESQ is an AI-assisted search-and-rescue system designed for disaster and flood-response scenarios.

The proposed system combines:

- UAV-based aerial reconnaissance
- AI-based person detection
- GPS-based geolocation
- Surface-buoy-assisted underwater reconnaissance
- Underwater camera and sonar sensing
- Sensor fusion
- A centralized rescue-intelligence dashboard

The current implementation is a software proof-of-concept using ROS 2, Gazebo, PX4 SITL, YOLOv8, and Streamlit.

---

## Current Working Prototype

The current software prototype demonstrates an integrated aerial perception pipeline using a simulated UAV.

The working pipeline consists of:

- Simulated UAV in Gazebo
- Simulated RGB camera
- ROS 2 image pipeline
- YOLOv8 person detection
- PX4 global-position data
- Detection geolocation
- JSON-based detection output
- Streamlit mission dashboard

When a person is detected in the simulated UAV camera, the system associates the detection with the UAV's simulated geographic position and writes the latest detection to:

```text
~/aqua_gazebo_test/latest_detections.json

The Streamlit dashboard reads this information and displays the detection and its location on the mission map.

Key Features
UAV-Based Reconnaissance

The proposed system uses a UAV for wide-area aerial reconnaissance during disaster-response operations.

The proposed UAV payload includes:

RGB camera
Thermal camera
GPS / RTK positioning
IMU
Onboard edge-computing hardware

The current software prototype demonstrates the RGB-camera perception pipeline in simulation.

AI-Based Person Detection

YOLOv8 is used to detect people in the simulated UAV camera feed.

For each detected person, the current prototype records:

Detection class
Confidence
Detection priority
Detection source
UAV geographic position
GPS-Based Geolocation

The simulated UAV receives global-position information from PX4.

The system uses:

Latitude
Longitude
Altitude

to associate a detected person with the UAV's simulated geographic location.

Mission Dashboard

The Streamlit dashboard provides a centralized interface for mission information.

It displays:

UAV and UUV status
Detection information
Detection confidence
Detection location
Mission map
Rescue intelligence
Resource allocation
Rescue recommendations
Communication status

The dashboard refreshes every 5 seconds.

Underwater Reconnaissance

The proposed system includes an underwater ROV supported by a surface buoy for targeted investigation of submerged areas.

The proposed underwater sensing system includes:

Underwater RGB / low-light camera
Imaging sonar
Depth / pressure sensor
IMU
DVL or acoustic positioning

The surface buoy is intended to provide a surface-level interface and communication relay for the underwater system.

The ROV is intended for targeted underwater investigation when aerial reconnaissance indicates that additional underwater information may be useful.

System Architecture

The proposed system consists of two coordinated operational domains.

Aerial System

The UAV performs aerial reconnaissance using cameras and onboard sensing. AI-based perception identifies potential survivors or hazards, and detected locations can be associated with the UAV's geographic position.

Surface Buoy

The surface buoy acts as the interface between the surface and underwater system. It is intended to support communication and coordination with the underwater ROV.

Underwater System

The underwater ROV performs targeted investigation of submerged areas using underwater cameras, imaging sonar, depth sensing, and underwater positioning methods.

Mission Dashboard

The mission dashboard provides a common interface for viewing detection information, vehicle status, map data, and rescue intelligence.

Technology Stack
Simulation
Ubuntu 24.04
ROS 2 Jazzy
Gazebo Harmonic
PX4 SITL
AI and Computer Vision
Python
YOLOv8
Ultralytics
OpenCV
CvBridge
Robotics and Communication
ROS 2
PX4
Micro XRCE-DDS
PX4 ROS 2 messages
Dashboard
Streamlit
Folium
streamlit-folium
streamlit-autorefresh
ROS 2 Package

The ROS 2 package is located at:

ros2_ws/src/aqua_resq/

The package contains:

package.xml
setup.py
setup.cfg
resource/
aqua_resq/

The Python package contains:

__init__.py
offboard_control.py
camera_viewer.py
offboard_control.py

Provides a ROS 2 offboard-control node for sending position setpoints to PX4.

camera_viewer.py

The perception node connects the simulated camera feed, YOLOv8 inference, and PX4 global-position data.

It performs the following operations:

Receives camera frames through ROS 2.
Converts ROS 2 images using CvBridge.
Runs YOLOv8 inference.
Identifies person detections.
Obtains the latest valid UAV position from PX4.
Associates the detection with the UAV position.
Saves the latest detection as JSON.
Displays the annotated camera feed.
Important ROS 2 Topics
Camera
/aqua_resq/camera/image
PX4 Global Position
/fmu/out/vehicle_global_position
PX4 Offboard Control
/fmu/in/offboard_control_mode
/fmu/in/trajectory_setpoint
/fmu/in/vehicle_command
Running the Dashboard

Create and activate the dashboard environment:

python3 -m venv ~/dashboard_env
source ~/dashboard_env/bin/activate

Install the required dependencies:

pip install -r requirements.txt

Run the dashboard:

cd AQUA-RESQ
streamlit run app.py

The dashboard can then be opened at:

http://localhost:8501
Running the ROS 2 Package

After installing ROS 2 Jazzy and the required PX4 dependencies:

cd ~/aqua_resq_ws
colcon build --packages-select aqua_resq
source install/setup.bash

Run the camera and detection node:

ros2 run aqua_resq camera_viewer

Run the offboard-control node:

ros2 run aqua_resq offboard_control
Detection Data

The latest detection is stored locally as:

~/aqua_gazebo_test/latest_detections.json

Example:

{
  "class": "person",
  "confidence": 0.90,
  "priority": "HIGH",
  "source": "UAV_Aerial_Cam",
  "bbox": [],
  "location": {
    "latitude": 47.397971,
    "longitude": 8.546163
  }
}

The JSON file is used to transfer the latest detection information from the ROS 2 perception pipeline to the Streamlit dashboard.

Project Status
Currently Demonstrated
UAV simulation
Gazebo camera simulation
ROS 2 camera pipeline
YOLOv8 person detection
PX4 global-position integration
Detection geolocation
JSON-based detection output
Streamlit mission dashboard
Proposed Future Hardware Implementation

The following components belong to the proposed physical system and are not represented as fully deployed hardware in the current software proof-of-concept:

Physical UAV
RGB and thermal camera payload
RTK positioning hardware
Surface buoy
Underwater ROV / UUV
Underwater imaging sonar
DVL / acoustic positioning
Physical communication infrastructure
Integrated aerial-underwater sensor fusion

The repository distinguishes between the current software prototype and the proposed future hardware system.

Mission Concept

The intended operational workflow is:

Detect potential survivors or hazards using aerial reconnaissance.
Associate detected targets with their geographic locations.
Prioritize targets using the available mission information.
Provide target information to the rescue team through the mission dashboard.
Deploy the underwater system when underwater investigation is required.
Use the surface buoy and ROV for targeted underwater reconnaissance.
Continue monitoring and update mission information as new detections become available.
Safety and Deployment Considerations

The current system is a simulation and software proof-of-concept.

A real-world deployment would require:

Hardware integration
Sensor calibration
Reliable communication links
Autonomous navigation validation
Fail-safe mechanisms
Waterproofing and pressure protection for underwater components
Field testing
Regulatory compliance
Human-supervised operational procedures

The simulated UAV, camera, GPS position, and detected targets should not be interpreted as measurements from a physical aircraft or deployed rescue system.

Disclaimer

This repository contains a simulation and software proof-of-concept for the AQUA-RESQ concept.

The current implementation demonstrates the software perception and mission-dashboard pipeline in simulation. The proposed physical UAV, surface buoy, underwater ROV, and associated sensors require further engineering, integration, testing, and field validation before real-world deployment.

References
PX4 Autopilot
ROS 2
Gazebo
Ultralytics YOLO
OpenCV
Streamlit
Folium
