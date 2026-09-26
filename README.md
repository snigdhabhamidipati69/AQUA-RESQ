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

The current implementation is a software proof-of-concept using ROS 2, Gazebo, PX4 SITL, YOLO, and Streamlit.

---

## Current Working Prototype

The current software pipeline demonstrates:

```text
Gazebo UAV
    ↓
RGB Camera
    ↓
ROS 2 Image Topic
    ↓
YOLOv8 Person Detection
    ↓
PX4 Global Position
    ↓
Detection JSON
    ↓
AQUA-RESQ Mission Dashboard

When a person is detected in the simulated UAV camera, the system associates the detection with the UAV's simulated geographic position and writes the latest detection to:

~/aqua_gazebo_test/latest_detections.json

The Streamlit dashboard reads this information and displays the detection on the mission map.

Key Features
1. UAV Simulation

The aerial vehicle is simulated using:

PX4 SITL
Gazebo Harmonic
ROS 2 Jazzy

The simulated UAV is equipped with an RGB camera.

2. AI Person Detection

YOLOv8 is used to detect people in the simulated camera feed.

The system records:

Detected class
Confidence
Detection priority
Detection source
UAV location
3. GPS Geolocation

The UAV's simulated PX4 global-position data is received through ROS 2.

The system uses:

Latitude
Longitude
Altitude

to associate a detected person with a geographic location.

4. Mission Dashboard

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

5. Underwater Reconnaissance Concept

The proposed system includes an underwater ROV supported by a surface buoy for targeted investigation of submerged areas.

The proposed underwater sensing system includes:

Underwater RGB / low-light camera
Imaging sonar
Depth / pressure sensor
IMU
DVL or acoustic positioning

The surface buoy provides a surface-level interface and communication relay for the underwater system.

The ROV is intended to investigate underwater areas when aerial reconnaissance indicates that further underwater information may be useful.

System Architecture
                 ┌─────────────────────┐
                 │      UAV / Drone    │
                 │                     │
                 │ RGB + Thermal Camera│
                 │ GPS / RTK + IMU     │
                 └──────────┬──────────┘
                            │
                            ▼
                     AI Perception
                       YOLOv8
                            │
                            ▼
                    Person / Hazard
                       Detection
                            │
                            ▼
                     Geo-tagging
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Mission Dashboard   │
                 │                     │
                 │ Map + Targets       │
                 │ Rescue Intelligence │
                 └──────────┬──────────┘
                            │
                    Underwater Cue
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Surface Buoy     │
                 │                     │
                 │ Communication Relay │
                 │ Surface Interface   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      UUV / ROV      │
                 │                     │
                 │ Camera + Sonar      │
                 │ Depth + IMU + DVL   │
                 └─────────────────────┘
Technology Stack
Simulation
Ubuntu 24.04
ROS 2 Jazzy
Gazebo Harmonic
PX4 SITL
AI / Computer Vision
Python
YOLOv8
Ultralytics
OpenCV
CvBridge
Robotics
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

It contains:

aqua_resq/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── aqua_resq
└── aqua_resq/
    ├── __init__.py
    ├── offboard_control.py
    └── camera_viewer.py
offboard_control.py

Provides a ROS 2 offboard-control node for sending position setpoints to PX4.

camera_viewer.py

Connects:

ROS 2 Camera
      +
PX4 Global Position
      +
YOLOv8

and produces dashboard-ready detection data.

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

Install dependencies:

pip install -r requirements.txt

Run:

cd AQUA-RESQ
streamlit run app.py

Then open:

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
Project Status
Currently demonstrated
UAV simulation
Gazebo camera simulation
ROS 2 camera pipeline
YOLOv8 person detection
PX4 global-position integration
Detection geolocation
JSON-based detection output
Streamlit mission dashboard
Proposed / Future Hardware Implementation

The following components are part of the proposed physical system and are not represented as fully deployed hardware in the current software proof-of-concept:

Physical UAV
RGB + thermal payload
RTK positioning hardware
Surface buoy
Underwater ROV / UUV
Underwater imaging sonar
DVL / acoustic positioning
Physical communication infrastructure
Integrated aerial-underwater sensor fusion

The repository therefore distinguishes between the current software prototype and the proposed future hardware system.

Mission Concept

The intended operational workflow is:

DETECT
   ↓
LOCATE
   ↓
PRIORITIZE
   ↓
DISPATCH
   ↓
INVESTIGATE
   ↓
RESCUE
   ↓
CONTINUE MONITORING

The UAV provides wide-area aerial reconnaissance.

When underwater information is required, the surface buoy and underwater ROV system can be deployed for targeted underwater investigation.

The mission dashboard provides a common interface for viewing detection and rescue information.

Disclaimer

This repository contains a simulation and software proof-of-concept for the AQUA-RESQ concept.

Simulation results should not be interpreted as validation of a real-world autonomous search-and-rescue system.

Real deployment would require additional testing, hardware integration, communication validation, safety mechanisms, regulatory compliance, and field trials.

References
PX4 Autopilot
ROS 2
Gazebo
Ultralytics YOLO
OpenCV
Streamlit
Folium
