import streamlit as st
import json
import os
import time
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------------
# AQUA-RESQ — Public Web Dashboard
# ---------------------------------------------------------

st.set_page_config(
    page_title="AQUA-RESQ Mission Control",
    page_icon="🚨",
    layout="wide",
)

st_autorefresh(interval=1000, key="datarefresh")

st.title("🚨 AQUA-RESQ Emergency Command & Intelligence Dashboard")
st.markdown("**Live UAV/ROV AI Perception, Localization & System Telemetry**")

# ---------------------------------------------------------
# DATA SOURCE
# ---------------------------------------------------------
# On the lab machine, the ROS 2 bridge can write to this file.
# Streamlit Cloud cannot access a file on your laptop, so the
# public deployment falls back to a clearly labelled simulation.
# ---------------------------------------------------------

LOCAL_JSON_PATH = os.path.expanduser(
    "~/aqua_gazebo_test/latest_detections.json"
)

DEMO_DETECTIONS = [
    {
        "class": "person",
        "confidence": 0.89,
        "priority": "HIGH",
        "source": "UAV_Aerial_Cam",
        "bbox": [337, 175, 397, 356],
        "location": {
            "latitude": 17.448976,
            "longitude": 78.391276,
        },
    }
]


def load_detections():
    """Load ROS2 bridge data locally; use demo data on public deployment."""
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

# ---------------------------------------------------------
# SIMULATED SYSTEM TELEMETRY
# ---------------------------------------------------------

elapsed_time = int(time.time()) % 100
sim_battery = max(15, 98 - int(elapsed_time * 0.5))

failsafe_status = (
    "NOMINAL" if sim_battery > 20 else "RTL (Return To Launch)"
)

flight_mode = (
    "AUTO_NAV" if sim_battery > 20 else "FAILSAFE_RTL"
)

# ---------------------------------------------------------
# TOP STATUS BAR
# ---------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    label="UAV Vision Feed",
    value="ACTIVE",
    delta="ROS 2 Jazzy",
)

col2.metric(
    label="Flight Mode",
    value=flight_mode,
    delta="PX4/Sim Nav",
)

col3.metric(
    label="UAV Battery",
    value=f"{sim_battery}%",
    delta="-0.5%/s" if sim_battery > 20 else "LOW BATTERY!",
    delta_color="normal" if sim_battery > 20 else "inverse",
)

col4.metric(
    label="Failsafe Status",
    value=failsafe_status,
    delta="System Ready" if sim_battery > 20 else "Auto Return Triggered",
    delta_color="normal" if sim_battery > 20 else "inverse",
)

if target_count == 0:
    col5.metric(
        label="Alert Level",
        value="NOMINAL",
        delta="Area Clear",
    )
else:
    col5.metric(
        label="Alert Level",
        value="HIGH PRIORITY" if target_count == 1 else "MASS CASUALTY",
        delta="Target Acquired" if target_count == 1 else "Critical Deployment",
    )

st.divider()

# Make the demo/local nature explicit instead of implying a live internet feed.
if data_source == "Public Demo / Simulated Data":
    st.info(
        "ℹ️ Public demonstration mode: detection, telemetry and GPS values "
        "are simulated. The local ROS 2 pipeline can feed the same dashboard "
        "when run on the simulation machine."
    )

if sim_battery <= 20:
    st.warning(
        "⚠️ **CRITICAL FAILSAFE ACTIVATED:** Battery below threshold (<20%). "
        "UAV auto-executing Return To Launch (RTL)."
    )

# ---------------------------------------------------------
# ACTIVE TARGET INTELLIGENCE + MAP
# ---------------------------------------------------------

if target_count > 0:

    left_col, right_col = st.columns([1, 1])

    with left_col:

        st.subheader("📋 Active Target Intelligence")

        for idx, det in enumerate(detections):

            target_class = str(det.get("class", "unknown")).upper()
            confidence = float(det.get("confidence", 0.0))
            priority = det.get("priority", "HIGH")
            source = det.get("source", "UAV_Aerial_Cam")
            bbox = det.get("bbox", [])

            location = det.get("location", {})
            lat = float(location.get("latitude", 0.0))
            lon = float(location.get("longitude", 0.0))

            st.error(
                f"**Target #{idx + 1} — {target_class} IDENTIFIED**"
            )

            m1, m2 = st.columns(2)

            m1.write(f"**Confidence:** {int(confidence * 100)}%")
            m1.write(f"**Priority:** {priority}")

            m2.write(f"**Source:** {source}")
            m2.write(
                f"**Simulated GPS:** `{lat:.6f}, {lon:.6f}`"
            )

            st.caption(f"Bounding Box (Pixels): {bbox}")

            if st.button(
                f"Dispatch Rescue Team to Target #{idx + 1}",
                key=f"dispatch_{idx}",
            ):
                st.success(
                    f"Rescue Unit Alpha dispatched to "
                    f"Lat {lat:.6f}, Lon {lon:.6f}!"
                )

            st.markdown("---")

        # -------------------------------------------------
        # DECISION SUPPORT
        # -------------------------------------------------

        st.subheader(
            "🏥 Automated Mission Decision & Resource Allocation"
        )

        st.info(
            "**Allocated Trauma Center:** "
            "Image Hospitals / Aashraya Hospitals "
            "(Simulated Proximity)"
        )

        st.warning(
            "**Recommended Resource:** "
            "1x Amphibious Rescue Craft + 2x Paramedic Units"
        )

    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    with right_col:

        st.subheader("🗺️ Live Tactical Rescue Map")

        first_location = detections[0].get("location", {})

        center_lat = float(first_location.get("latitude", 17.448976))
        center_lon = float(first_location.get("longitude", 78.391276))

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=17,
        )

        for idx, det in enumerate(detections):

            location = det.get("location", {})

            lat = float(location.get("latitude", center_lat))
            lon = float(location.get("longitude", center_lon))

            target_class = det.get("class", "target")
            confidence = float(det.get("confidence", 0.0))

            folium.Marker(
                [lat, lon],
                popup=(
                    f"Target #{idx + 1}: "
                    f"{target_class} "
                    f"({int(confidence * 100)}%)"
                ),
                tooltip=f"🚨 TARGET #{idx + 1} IDENTIFIED",
                icon=folium.Icon(
                    color="red",
                    icon="user",
                    prefix="fa",
                ),
            ).add_to(m)

        st_folium(
            m,
            width=None,
            height=450,
        )

else:

    st.success(
        "✅ Scanning water sector... "
        "No victims detected in camera field of view."
    )
