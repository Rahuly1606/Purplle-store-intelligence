import json
import streamlit as st
from PIL import Image

from utils import load_json, get_image_path, get_video_path
from charts import (
    dwell_chart,
    zone_visits_chart,
    funnel_chart,
    occupancy_chart,
    journeys_table,
)

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide",
    page_icon="🏪",
)

# ── load data ────────────────────────────────────────────────
metrics = load_json("outputs/store_metrics.json")
report  = load_json("outputs/final_report.json")
heatmap_path = get_image_path("outputs/heatmap.png")
video_path   = get_video_path("outputs/annotated_store_video.mp4")

# ── header ───────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='text-align:center; color:#4361ee;'>🏪 Store Intelligence Dashboard</h1>
    <p style='text-align:center; color:#6c757d; font-size:18px;'>
        Retail Analytics and Customer Behavior Insights
    </p>
    <hr/>
    """,
    unsafe_allow_html=True,
)

if metrics is None:
    st.error(
        "⚠️ No metrics found. Run the pipeline first: "
        "`python -m pipeline.main_pipeline`"
    )
    st.stop()

# ── sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.image(heatmap_path) if heatmap_path else st.info("No heatmap yet")
    st.markdown("### 📊 Dashboard Overview")
    st.metric("Total Visitors",  metrics.get("total_visitors", 0))
    st.metric("Total Zones",     len(metrics.get("zone_visits", {})))
    st.markdown("---")
    st.caption("Store Intelligence Platform")

# ═════════════════════════════════════════════════════════════
# SECTION 1 — EXECUTIVE OVERVIEW
# ═════════════════════════════════════════════════════════════
st.markdown("## 📈 Executive Overview")

total     = metrics.get("total_visitors", 0)
customers = metrics.get("customer_count", 0)
staff     = metrics.get("staff_count", 0)
conv_dict = metrics.get("conversion_rate", {})
conv_rate = conv_dict.get("FOH_TO_CASH_COUNTER", 0)
peak_occ  = metrics.get("peak_occupancy", {})
peak_max  = max(peak_occ.values(), default=0)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👥 Total Visitors",  total)
c2.metric("🛍️ Customers",       customers)
c3.metric("👔 Staff",           staff)
c4.metric("💰 Conversion Rate", f"{conv_rate*100:.1f}%")
c5.metric("📍 Peak Occupancy",  peak_max)

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 2 — DWELL ANALYTICS
# ═════════════════════════════════════════════════════════════
st.markdown("## ⏱️ Dwell Analytics")

avg_dwell = metrics.get("avg_dwell_time", {})

if avg_dwell:
    st.plotly_chart(
        dwell_chart(avg_dwell),
        use_container_width=True,
    )
else:
    st.info("No dwell data available.")

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 3 — ZONE VISITS
# ═════════════════════════════════════════════════════════════
st.markdown("## 🗺️ Zone Visits")

zone_visits = metrics.get("zone_visits", {})

if zone_visits:
    st.plotly_chart(
        zone_visits_chart(zone_visits),
        use_container_width=True,
    )
else:
    st.info("No zone visit data available.")

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 4 — CONVERSION FUNNEL
# ═════════════════════════════════════════════════════════════
st.markdown("## 🔻 Conversion Funnel")

zone_funnel = metrics.get("zone_funnel", {})

if zone_funnel:
    st.plotly_chart(
        funnel_chart(zone_funnel, conv_dict),
        use_container_width=True,
    )
else:
    st.info("No funnel data available.")

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 5 — OCCUPANCY ANALYTICS
# ═════════════════════════════════════════════════════════════
st.markdown("## 🏠 Peak Occupancy by Zone")

if peak_occ:
    st.plotly_chart(
        occupancy_chart(peak_occ),
        use_container_width=True,
    )
else:
    st.info("No occupancy data available.")

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 6 — VISITOR JOURNEYS
# ═════════════════════════════════════════════════════════════
st.markdown("## 🚶 Visitor Journeys")

visitor_paths = metrics.get("visitor_paths", {})

if visitor_paths:
    df = journeys_table(visitor_paths)
    search = st.text_input("🔍 Filter by Visitor ID", "")

    if search:
        df = df[
            df["Visitor ID"].str.contains(
                search, case=False
            )
        ]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No journey data available.")

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 7 — HEATMAP
# ═════════════════════════════════════════════════════════════
st.markdown("## 🌡️ Customer Engagement Heatmap")

if heatmap_path:
    img = Image.open(heatmap_path)
    st.image(img, use_container_width=True)
else:
    st.warning("Heatmap not found at `outputs/heatmap.png`.")

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 8 — VIDEO VERIFICATION
# ═════════════════════════════════════════════════════════════
st.markdown("## 🎥 Annotated Store Video")

if video_path:
    with open(video_path, "rb") as vf:
        st.video(vf.read())
else:
    st.warning(
        "Annotated video not found at "
        "`outputs/annotated_store_video.mp4`."
    )

st.markdown("---")

# ═════════════════════════════════════════════════════════════
# SECTION 9 — RAW METRICS
# ═════════════════════════════════════════════════════════════
st.markdown("## 🗂️ Raw Report Data")

with st.expander("View final_report.json", expanded=False):
    if report:
        st.json(report)
    else:
        st.info("final_report.json not found.")
