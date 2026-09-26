import streamlit as st
import json
import os
import time
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="AQUA-RESQ Mission Control", page_icon="", layout="wide")
st_autorefresh(interval=5000, key="datarefresh")

if "mission_started" not in st.session_state:
    st.session_state.mission_started = False
if "dispatch_clicked" not in st.session_state:
    st.session_state.dispatch_clicked = False

LOCAL_JSON_PATH = os.path.expanduser("~/aqua_gazebo_test/latest_detections.json")
DEMO_DETECTIONS = [{
    "class": "person",
    "confidence": 0.89,
    "priority": "HIGH",
    "source": "UAV_Aerial_Cam",
    "bbox": [337, 175, 397, 356],
    "location": {"latitude": 17.448976, "longitude": 78.391276}
}]

def load_detections():
    if os.path.exists(LOCAL_JSON_PATH):
        try:
            with open(LOCAL_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                data = [data]
            if isinstance(data, list):
                return data, "ROS 2 / Local Simulation"
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    return DEMO_DETECTIONS, "Public Demo / Simulated Data"

detections, data_source = load_detections()
target_count = len(detections)

st.title("AQUA-RESQ Emergency Command & Intelligence Dashboard")
st.markdown("**Live UAV/ROV AI Perception, Localization & System Telemetry**")

elapsed_time = int(time.time()) % 100
sim_battery = max(15, 98 - int(elapsed_time * 0.5))
failsafe_status = "NOMINAL" if sim_battery > 20 else "RTL (Return To Launch)"
flight_mode = "AUTO_NAV" if sim_battery > 20 else "FAILSAFE_RTL"

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("UAV Vision Feed", "ACTIVE" if st.session_state.mission_started else "STANDBY", "ROS 2 Jazzy")
c2.metric("Flight Mode", flight_mode if st.session_state.mission_started else "STANDBY", "PX4/Sim Nav")
c3.metric("UAV Battery", f"{sim_battery}%" if st.session_state.mission_started else "100%", "-0.5%/s" if st.session_state.mission_started else "Ready")
c4.metric("Failsafe Status", failsafe_status if st.session_state.mission_started else "NOMINAL", "System Ready")
c5.metric("Alert Level", ("HIGH PRIORITY" if target_count == 1 else "MASS CASUALTY") if st.session_state.mission_started and target_count else "NOMINAL", "Target Acquired" if st.session_state.mission_started and target_count else "Standby")
st.divider()

if data_source == "Public Demo / Simulated Data":
    st.info("ℹ️ **Public demonstration mode:** detection, telemetry and GPS values are simulated. The local ROS 2 pipeline can feed the same dashboard when run on the simulation machine.")

st.subheader("Mission Control")
mc1,mc2,mc3,mc4 = st.columns(4)
with mc1:
    if st.button("START MISSION", use_container_width=True):
        st.session_state.mission_started = True
with mc2:
    if st.button("RESET MISSION", use_container_width=True):
        st.session_state.mission_started = False
        st.session_state.dispatch_clicked = False
with mc3:
    st.metric("Drone", "ACTIVE" if st.session_state.mission_started else "STANDBY")
with mc4:
    st.metric("UUV", "ACTIVE" if st.session_state.mission_started else "STANDBY")
if st.session_state.mission_started:
    st.success("✅Mission started — multi-agent flood reconnaissance active.")
st.divider()

# Full disaster map plus new detection marker
left,right = st.columns([2,1])
with left:
    st.subheader("🗺️ Live Disaster Zone")
    st.caption("⚠️ Prototype simulation — locations, routes and detections are simulated.")
    m = folium.Map(location=[17.3850,78.4867], zoom_start=13)
    folium.Marker([17.3900,78.4800], popup="Aerial Drone", tooltip="Drone",
                  icon=folium.Icon(icon="send", prefix="fa")).add_to(m)
    folium.Marker([17.3780,78.4920], popup="Underwater Vehicle", tooltip="UUV",
                  icon=folium.Icon(icon="tint", prefix="fa")).add_to(m)
    if st.session_state.mission_started:
        folium.Marker([17.3820,78.4880], popup="👤 Possible Survivor",
                      tooltip="Survivor Detected",
                      icon=folium.Icon(color="red", icon="user")).add_to(m)
        for i,det in enumerate(detections):
            loc=det.get("location",{})
            lat=float(loc.get("latitude",17.448976)); lon=float(loc.get("longitude",78.391276))
            folium.Marker([lat,lon],
                popup=f"Target #{i+1}: {det.get('class','target')} ({int(float(det.get('confidence',0))*100)}%)",
                tooltip=f"🚨 TARGET #{i+1} IDENTIFIED",
                icon=folium.Icon(color="red",icon="user",prefix="fa")).add_to(m)
    folium.Marker([17.3870,78.4950], popup="⚠️ Flood Hazard", tooltip="Hazard",
                  icon=folium.Icon(color="orange",icon="warning-sign")).add_to(m)
    flood_zone=[[17.394,78.475],[17.398,78.490],[17.388,78.502],[17.375,78.497],[17.370,78.482],[17.382,78.470]]
    folium.Polygon(flood_zone,color="blue",fill=True,fill_color="blue",fill_opacity=0.25,popup="Flood-affected zone").add_to(m)
    route=[[17.3900,78.4800],[17.3860,78.4840],[17.3820,78.4880]]
    folium.PolyLine(route,color="green",weight=5,popup="Recommended rescue route").add_to(m)
    st_folium(m,width=None,height=500)
with right:
    st.subheader("🚨 Alerts")
    if st.session_state.mission_started:
        if target_count:
            st.error(f"👤 {target_count} target(s) detected — Priority: {detections[0].get('priority','HIGH')}")
        st.warning("⚠️ Flood hazard detected near rescue zone")
        st.info("UUV investigating submerged objects")
    else:
        st.success("No active mission alerts")
st.divider()

st.subheader("📋 Active Target Intelligence")
if st.session_state.mission_started and target_count:
    for i,det in enumerate(detections):
        target_class=str(det.get("class","unknown")).upper()
        confidence=float(det.get("confidence",0))
        priority=det.get("priority","HIGH")
        source=det.get("source","UAV_Aerial_Cam")
        bbox=det.get("bbox",[])
        loc=det.get("location",{})
        lat=float(loc.get("latitude",17.448976)); lon=float(loc.get("longitude",78.391276))
        st.error(f"**Target #{i+1} — {target_class} IDENTIFIED**")
        a,b=st.columns(2)
        a.write(f"**Confidence:** {int(confidence*100)}%")
        a.write(f"**Priority:** {priority}")
        b.write(f"**Source:** {source}")
        b.write(f"**Simulated GPS:** `{lat:.6f}, {lon:.6f}`")
        st.caption(f"Bounding Box (Pixels): {bbox}")
        if st.button(f"Dispatch Rescue Team to Target #{i+1}",key=f"dispatch_{i}",use_container_width=True):
            st.session_state.dispatch_clicked=True
            st.success(f"Rescue Unit Alpha dispatched to Lat {lat:.6f}, Lon {lon:.6f}!")
else:
    st.info("Start the mission to display active AI targets.")
st.divider()

st.subheader("Vehicle Status")
a,b=st.columns(2)
with a:
    st.markdown("### Aerial Drone")
    st.write(f"Status: **{'ACTIVE' if st.session_state.mission_started else 'STANDBY'}**")
    st.write(f"Battery: **{'87%' if st.session_state.mission_started else '100%'}**")
    st.write(f"Altitude: **{'80 m' if st.session_state.mission_started else '0 m'}**")
    st.write("Navigation: **GPS / RTK + IMU (simulated)**")
with b:
    st.markdown("### Underwater Vehicle")
    st.write(f"Status: **{'ACTIVE' if st.session_state.mission_started else 'STANDBY'}**")
    st.write(f"Battery: **{'82%' if st.session_state.mission_started else '100%'}**")
    st.write(f"Depth: **{'8 m' if st.session_state.mission_started else '0 m'}**")
    st.write("Navigation: **INS + Sonar (simulated)**")
st.divider()

st.subheader("AI Detection & Analysis")
a,b,c,d=st.columns(4)
a.metric("👤 Survivors",str(target_count) if st.session_state.mission_started else "0")
b.metric("⚠️ Hazards","2" if st.session_state.mission_started else "0")
c.metric("🌊 Submerged Objects","3" if st.session_state.mission_started else "0")
d.metric("🎯 Critical Targets","1" if st.session_state.mission_started and target_count else "0")
st.divider()

st.subheader("Rescue Intelligence")
a,b,c=st.columns(3)
a.metric("Highest Priority","Survivor #01" if st.session_state.mission_started else "None")
b.metric("Detection Confidence",f"{int(float(detections[0].get('confidence',0))*100)}%" if st.session_state.mission_started and target_count else "—")
c.metric("Rescue Priority","CRITICAL" if st.session_state.mission_started else "—")
st.divider()

st.subheader("AI Detection Feed")
a,b=st.columns(2)
with a:
    st.markdown("### Drone — Aerial View")
    if st.session_state.mission_started and target_count:
        det=detections[0]; loc=det.get("location",{})
        st.success("👤 Survivor / Person detected")
        st.write(f"Confidence: **{int(float(det.get('confidence',0))*100)}%**")
        st.write(f"Location: **{float(loc.get('latitude',17.448976)):.6f}, {float(loc.get('longitude',78.391276)):.6f}**")
        st.write("Classification: **Person / High Priority**")
        st.write(f"Bounding Box: **{det.get('bbox',[])}**")
    else: st.info("Drone camera standby")
with b:
    st.markdown("### UUV — Underwater View")
    if st.session_state.mission_started:
        st.warning("⚠️ Submerged objects detected")
        st.write("Objects detected: **3**")
        st.write("Depth: **8 m**")
        st.write("Navigation: **INS + Sonar**")
    else: st.info("UUV camera standby")
st.divider()

st.subheader("Automated Mission Decision & Resource Allocation")
if st.session_state.mission_started:
    st.info("**Allocated Trauma Center:** Image Hospitals / Aashraya Hospitals (Simulated Proximity)")
    st.warning("**Recommended Resource:** 1x Amphibious Rescue Craft + 2x Paramedic Units")
    if st.session_state.dispatch_clicked:
        st.success("Rescue dispatch command recorded for the active target.")
else:
    st.info("Start the mission to generate mission recommendations.")
st.divider()

st.subheader("Rescue Recommendation")
if st.session_state.mission_started:
    st.success("Recommended Action: Deploy rescue team to Survivor #01 using the green route shown on the map.")
    if target_count:
        loc=detections[0].get("location",{})
        st.write(f"📍 Target: {float(loc.get('latitude',17.448976)):.6f}, {float(loc.get('longitude',78.391276)):.6f}")
    st.write("⚠️ Avoid detected flood hazard at 17.3870, 78.4950")
else:
    st.info("Start the mission to generate rescue recommendations.")
st.divider()

st.subheader("Mission Timeline")
if st.session_state.mission_started:
    st.write("✅ **T+00:00** — Mission initiated")
    st.write("🚁 **T+00:15** — Drone began aerial flood reconnaissance")
    st.write("👤 **T+00:32** — Survivor detected with 89% confidence")
    st.write("🌊 **T+00:45** — UUV deployed for underwater verification")
    st.write("⚠️ **T+01:02** — Flood hazard identified")
    st.write("🎯 **T+01:15** — Survivor classified as HIGH priority")
    st.write("🛟 **T+01:25** — Recommended rescue route generated")
else: st.info("Start the mission to view mission events.")
st.divider()

st.subheader("Emergency Response")
a,b,c=st.columns(3)
with a:
    st.markdown("### 👥 Rescue Volunteers")
    if st.session_state.mission_started:
        st.metric("Available Teams","4"); st.write("Personnel available: **12**"); st.success("Team Alpha assigned to Survivor #01")
    else:
        st.metric("Available Teams","—"); st.write("Start mission to assign rescue teams.")
with b:
    st.markdown("### 🧰 Rescue Equipment")
    if st.session_state.mission_started:
        st.write("🪢 Rescue ropes: **6**"); st.write("🦺 Life jackets: **8**"); st.write("🛟 Inflatable stretcher: **2**"); st.write("🩹 First-aid kits: **4**")
    else: st.info("Equipment status unavailable")
with c:
    st.markdown("### 🏥 Medical Support")
    if st.session_state.mission_started:
        st.success("Operational"); st.write("Nearest Hospital: **2.4 km**"); st.write("Emergency capacity: **Available**"); st.write("ETA: **8 min**")
    else: st.info("Start mission to locate medical support.")
st.divider()

st.subheader("Communication & System Status")
a,b,c,d=st.columns(4)
a.metric("Edge AI","ACTIVE" if st.session_state.mission_started else "STANDBY")
b.metric("Network","LIMITED" if st.session_state.mission_started else "STANDBY")
c.metric("Local Processing","ON" if st.session_state.mission_started else "OFF")
d.metric("Data Sync","ACTIVE" if st.session_state.mission_started else "—")
st.divider()

st.subheader("Rescue Team Assignment")
if st.session_state.mission_started:
    a,b,c=st.columns(3)
    with a:
        st.markdown("### 👥 Team Alpha"); st.success("EN ROUTE"); st.write("Personnel: **3**"); st.write("ETA: **6 min**")
    with b:
        st.markdown("### 🧰 Equipment"); st.write("🪢 Rescue rope"); st.write("🦺 Life jackets"); st.write("🛟 Inflatable stretcher")
    with c:
        st.markdown("### 🎯 Assignment"); st.write("Target: **Survivor #01**"); st.write("Priority: **HIGH**"); st.write("Route: **Recommended**")
else:
    st.info("Start mission to assign rescue teams.")
