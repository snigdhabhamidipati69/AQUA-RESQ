import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="AQUA-RESQ",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 AQUA-RESQ")
st.caption("AI-Powered Multi-Agent Flood Disaster Response System")
if "mission_started" not in st.session_state:
    st.session_state.mission_started = False

if st.button("🚀 START MISSION"):
    st.session_state.mission_started = True

if st.session_state.mission_started:
    st.success("Mission started!")

st.divider()

# Mission Control
st.subheader("🎯 Mission Control")

col1, col2, col3, col4 = st.columns(4)

with col1:
    drone_status = "ACTIVE" if st.session_state.mission_started else "STANDBY"
    st.metric("🚁 Drone", drone_status)

with col2:
    uuv_status = "ACTIVE" if st.session_state.mission_started else "STANDBY"
    st.metric("🌊 UUV", uuv_status)

with col3:
    flood_status = "ASSESSING" if st.session_state.mission_started else "HIGH"
    st.metric("🌊 Flood Severity", flood_status)

with col4:
    alert_count = "0"
    st.metric("🚨 Active Alerts", alert_count)

st.divider()

# Main dashboard
left, right = st.columns([2, 1])

with left:
    st.subheader("🗺️ Live Disaster Zone")
    st.caption("⚠️ Prototype simulation — locations and detections are simulated.")

    # Create map
    m = folium.Map(
        location=[17.3850, 78.4867],
        zoom_start=13
    )

    # Drone marker
    folium.Marker(
        [17.3900, 78.4800],
        popup="🚁 Aerial Drone",
        tooltip="Drone",
        icon=folium.Icon(icon="send", prefix="fa")
    ).add_to(m)

    # UUV marker
    folium.Marker(
        [17.3780, 78.4920],
        popup="🌊 Underwater Vehicle",
        tooltip="UUV",
        icon=folium.Icon(icon="tint", prefix="fa")
    ).add_to(m)

    # Survivor
    # Survivor
if st.session_state.mission_started:
    folium.Marker(
        [17.3820, 78.4880],
        popup="👤 Possible Survivor",
        tooltip="Survivor Detected",
        icon=folium.Icon(color="red", icon="user")
    ).add_to(m)

    # Hazard
    folium.Marker(
        [17.3870, 78.4950],
        popup="⚠️ Flood Hazard",
        tooltip="Hazard",
        icon=folium.Icon(color="orange", icon="warning-sign")
    ).add_to(m)

        # Simulated flooded zone
    flood_zone = [
        [17.394, 78.475],
        [17.398, 78.490],
        [17.388, 78.502],
        [17.375, 78.497],
        [17.370, 78.482],
        [17.382, 78.470]
    ]

    folium.Polygon(
        locations=flood_zone,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.25,
        popup="🌊 Flood-affected zone"
    ).add_to(m)

    # Mission route
    route = [
        [17.3900, 78.4800],
        [17.3860, 78.4840],
        [17.3820, 78.4880]
    ]

    folium.PolyLine(
        route,
        color="green",
        weight=5,
        popup="Recommended rescue route"
    ).add_to(m)

    st_folium(
        m,
        width=None,
        height=500
    )

with right:
    st.subheader("🚨 Alerts")

    if st.session_state.mission_started:
        st.error("👤 Survivor detected — Priority: HIGH")
        st.warning("⚠️ Flood hazard detected near rescue zone")
        st.info("🌊 UUV investigating submerged objects")
    else:
        st.success("No critical alerts")

st.divider()

# Vehicle Status
st.subheader("🤖 Vehicle Status")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚁 Aerial Drone")
    drone_vehicle_status = "ACTIVE" if st.session_state.mission_started else "STANDBY"
    st.write(f"Status: **{drone_vehicle_status}**")
    drone_battery = "87%" if st.session_state.mission_started else "100%"
    st.write(f"Battery: **{drone_battery}**")
    drone_altitude = "80 m" if st.session_state.mission_started else "0 m"
    st.write(f"Altitude: **{drone_altitude}**")
    st.write("Navigation: **GPS**")

with col2:
    st.markdown("### 🌊 Underwater Vehicle")
    uuv_vehicle_status = "ACTIVE" if st.session_state.mission_started else "STANDBY"
    st.write(f"Status: **{uuv_vehicle_status}**")
    uuv_battery = "82%" if st.session_state.mission_started else "100%"
    st.write(f"Battery: **{uuv_battery}**")
    uuv_depth = "8 m" if st.session_state.mission_started else "0 m"
    st.write(f"Depth: **{uuv_depth}**")
    st.write("Navigation: **INS + Sonar**")

st.divider()

# AI Detection
st.subheader("🤖 AI Detection & Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    survivor_count = "1" if st.session_state.mission_started else "0"
    st.metric("👤 Survivors", survivor_count)

with col2:
    hazard_count = "2" if st.session_state.mission_started else "0"
    st.metric("⚠️ Hazards", hazard_count)

with col3:
    submerged_count = "3" if st.session_state.mission_started else "0"
    st.metric("🌊 Submerged Objects", submerged_count)

with col4:
    critical_count = "1" if st.session_state.mission_started else "0"
    st.metric("🎯 Critical Targets", critical_count)

st.divider()

# Rescue Intelligence
st.subheader("🧠 Rescue Intelligence")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎯 Highest Priority",
        "Survivor #01" if st.session_state.mission_started else "None"
    )

with col2:
    st.metric(
        "📊 Detection Confidence",
        "94%" if st.session_state.mission_started else "—"
    )

with col3:
    st.metric(
        "🛟 Rescue Priority",
        "CRITICAL" if st.session_state.mission_started else "—"
    )

st.divider()

# AI Camera Feed
st.subheader("📹 AI Detection Feed")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚁 Drone — Aerial View")

    if st.session_state.mission_started:
        st.success("👤 Survivor detected")
        st.write("Confidence: **94%**")
        st.write("Location: **17.3820, 78.4880**")
        st.write("Classification: **Person / High Priority**")
    else:
        st.info("Drone camera standby")

with col2:
    st.markdown("### 🌊 UUV — Underwater View")

    if st.session_state.mission_started:
        st.warning("⚠️ Submerged objects detected")
        st.write("Objects detected: **3**")
        st.write("Depth: **8 m**")
        st.write("Navigation: **INS + Sonar**")
    else:
        st.info("UUV camera standby")

st.divider()

# Rescue Recommendation
st.subheader("🛟 Rescue Recommendation")

if st.session_state.mission_started:
    st.success(
        "Recommended Action: Deploy rescue team to Survivor #01 "
        "using the green route shown on the map."
    )
    st.write("📍 Target: 17.3820, 78.4880")
    st.write("⚠️ Avoid detected flood hazard at 17.3870, 78.4950")
else:
    st.info("Start the mission to generate rescue recommendations.")

st.divider()

# Mission Timeline
st.subheader("⏱️ Mission Timeline")

if st.session_state.mission_started:
    st.write("✅ **T+00:00** — Mission initiated")
    st.write("🚁 **T+00:15** — Drone began aerial flood reconnaissance")
    st.write("👤 **T+00:32** — Survivor detected with 94% confidence")
    st.write("🌊 **T+00:45** — UUV deployed for underwater verification")
    st.write("⚠️ **T+01:02** — Flood hazard identified")
    st.write("🎯 **T+01:15** — Survivor classified as CRITICAL priority")
    st.write("🛟 **T+01:25** — Recommended rescue route generated")
else:
    st.info("Start the mission to view mission events.")